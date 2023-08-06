import pyopencl as cl
import numpy as np
import scipy
from scipy.sparse import csr_matrix
from gpuinfo import GPUInfo as g
#import gpuadder - that was our cuda package, which is important in this 
#     in this file, because that here is the "save version", not the opencl-only version
import time
#import collapse

#from pynvml import * - hopefully we can comment that out, I have no idea, what that is

import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '0'
os.environ['PYOPENCL_CTX'] = '0'

# todo: give better names for "multiply_clTotal" etc.
#     ; actually, they calculate the entire levenshtein 
#     distance directly

def multiply_clTotal(a, b, gpu_l, threshold):
    """
    info:  arrays a and b of strings
    input: a: array of strings
        b: array of strings
        gpu_l: sidelength of the tiles in which the 
            matrix is divided for the gpu calculation.
            (the total matrix is too big to save it on the 
            GPU as a hole) (technical value)

            recommended gpu_l for levenshtein: gpu_l = 35000
        threshold: maximum jaccard distance, which is called
            connected (usually between 0 and 1)
    output: distance matrix as sparse csr_matrix 
    """
    # todo: are a and b arrays of strings or of what?

    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: starting multiply_clTotal ...")
    sz_a = a.shape
    sz_b = b.shape
    # perhaps make a check, that the matrix sizes are appropriate
    (n, m, p) = (sz_a[0], sz_a[1], sz_b[1])
    
    n_steps = int(n/gpu_l - (n%gpu_l)/gpu_l)
    m_steps = int(m/gpu_l - (m%gpu_l)/gpu_l)
    p_steps = int(p/gpu_l - (p%gpu_l)/gpu_l)
    #c = np.zeros([n, p])
    c = scipy.sparse.csr_matrix((n, p), dtype=np.int)

    if n%gpu_l > 0:
        n_steps += 1

    if m%gpu_l > 0:
        m_steps += 1

    if p%gpu_l > 0:
        p_steps += 1

    idxs_all = np.array([])
    cols_all = np.array([])
    vals_all = np.array([])

    for i in range(n_steps):
        for k in range(p_steps): 
            for j in range(m_steps):
                # info: index of the row in matrix A
                if not i == (n_steps-1):
                    i_down = i*gpu_l
                    i_up = (i+1)*gpu_l
                else: 
                    i_down = i*gpu_l
                    i_up = n

                # info: index of the column in matrix B
                if not k==(p_steps-1):
                    k_down = k*gpu_l
                    k_up = (k+1)*gpu_l
                else: 
                    k_down = k*gpu_l
                    k_up = p

                # info: index of the "product block"
                if not j==(m_steps-1): 
                    j_down = j*gpu_l
                    j_up = (j+1)*gpu_l
                else: 
                    j_down = j*gpu_l
                    j_up = m

                print("\n i_down: ", i_down, "; i_up: ", i_up, "; k_down: ", k_down, "; k_up: ", k_up, "; j_down: ", j_down, "; j_up: ", j_up)
                #c[i_down:i_up, k_down:k_up] = multiply_cl(a[i_down:i_up, j_down:j_up], b[j_down:j_up, k_down:k_up])
                idxs, cols, vals = multiply_cl(a[i_down:i_up, j_down:j_up], b[j_down:j_up, k_down:k_up], gpu_l, i, k, threshold)
                idxs_all = np.concatenate((np.array(idxs_all, dtype=np.int), np.array(idxs, dtype=np.int)))
                cols_all = np.concatenate((np.array(cols_all, dtype=np.int), np.array(cols, dtype=np.int)))
                vals_all = np.concatenate((np.array(vals_all), np.array(vals)))
    """if len(vals_all) == 0:
        c = None
    else:
        c = csr_matrix((vals_all, (idxs_all, cols_all))).toarray()
    return c
    """
    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py finished multiply_clTotal")
    return idxs_all, cols_all, vals_all
def make_indices_normal(cols, control_length):
    """
    info: take the sparce-csr indices and convert them to normal
        sparse indices
    input: cols: csr-sparse indices
        control_length: total number of nonzero elements in the 
            matrix
    output: col_normal: normal sparse indices
    """
    col_normal = list()
    len_cols = len(cols) 

    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py starting ...")
    
    for i in range(len_cols): 
        if (i > 0) and (cols[i] - cols[i-1] > 0):
            for j in range(cols[i]-cols[i-1]):
                col_normal.append(i-1)
    # hopefully, that is correct:
    for j in range(control_length - cols[len_cols-1]):
        col_normal.append(len_cols-1)

    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py ending")
    """
    if (control_length == len(col_normal)):
        print("\n The lengths are okay; " \
                " control_length: " + str(control_length) + "; len(col_normal): " \
                + str(len(col_normal))
                )
    else:
        print("\n (paul) Error: col_normal has the wrong length, \
                control_length: " + str(control_length) + "; len(col_normal): " \
                 + str(len(col_normal)))
    """
    return col_normal

def multiply_cl(a, b, gpu_l, i, k, threshold): 
    """
    info: calculate the matrix product of two matrices a and b on the GPU by using OpenCL
    input: a: matrix
        b: matrix
        gpu_l: sidelength of the gpu block
        i: index of block in x direction
        k: index of block in y direction
        threshold: maximum jaccard distance, which is called
            connected (usually between 0 and 1)
    output: product of a and b
    """    
    # do we have to cite the source?
    #a = np.matrix(a)
    #b = np.matrix(b)
    #a = scipy.sparse.csr_matrix.todense(a)
    #b = scipy.sparse.csr_matrix.todense(b)

    sz_a = a.shape
    sz_b = b.shape
    (n, m, p) = (sz_a[0], sz_a[1], sz_b[1])

    #c = np.zeros((n*p), dtype=np.float32)
    c = np.zeros((n*p), dtype=np.float32)
    
    a = np.reshape(a, n*m)
    b = np.reshape(b, m*p)

    a = a.astype(np.float32)
    b = b.astype(np.float32)
    
    #ctx = cl.create_some_context()
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)

    queue = cl.CommandQueue(ctx)
    
    mf = cl.mem_flags
    a_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer\
       (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)
    
    # pay attention: we have added the line "c"          if (c[gid] > 10)
    #      {c[gid] = 1}
    #      else
    #      {c[gid] = 0}
    # in for testing reasons, that should be corrected later
    
    prg = cl.Program(ctx, """
        __kernel void multiply(ushort n,
        ushort m, ushort p, __global float *a,
        __global float *b, __global float *c, float threshold)
        {
          int gid = get_global_id(0);
          
          //printf(" -- gid: %i, a[i]: %i", gid, a[gid]);
          //printf(" - b[i]: %i", b[gid]);

          /*printf(" --- a; 0: %f", a[0]);
          printf(" - 1: %f", a[1]);
          printf(" - 2: %f", a[2]);
          printf(" - 3: %f", a[3]);
          printf(" - 4: %f", a[4]);
          printf(" - 5: %f", a[5]);
          */
          c[gid] = 0.0f;
          int rowC = gid/n; // p
          int colC = gid%n; // p
          //printf("--- gid: %i, rowC*m: %i, colC: %i : ", gid, rowC*m, colC);
          //printf("--- a[rowC*m]: %i, b[colC]: %i", a[rowC*m], b[colC]);
          //__global int *pA; // &a[rowC*m];
          //__global int *pB; // = &b[colC];
          int pA;
          int pB;

          float m_float = (float) m;
          float c_intersection = 0.0f;
          float c_unity = 0.0f;
          float c_fraction = 0.0f;
          for(int k=0; k<m; k++)
          {
             
             pA = ((int)(a[rowC*m+k]));
             pB = ((int)(b[colC+k*p]));

             /*c_intersection += (*(pA++))*(*pB);
             c_unity += (1.0 - *pA++)*(1.0 - *pB);*/
             
             //if (((pA++))&&(pB))
             if (pA*pB == 1)
             {c_intersection += 1;
             }
             //if (((pA++))||(pB))
             if (1 - (1-pA)*(1-pB) == 1)
             {c_unity += 1;}
             /*
             if (gid == 3)
             {
                 printf("--- gid: %i", gid);
                 printf("--- rowC+k: %i", rowC*m+k);
                 printf("--- colC+k: %i", colC+k*p);
                 printf("--- pA: %i", pA);
                 printf("--- pB: %i", pB);
                 //printf("--- int: %i", ((int)(a[rowC*m+k])));
                 //printf("--- int: %i", ((int)(b[colC+k*p])));
                 printf("--- pA&&pB: %i", (pA*pB));
                 printf("--- pA||pB: %i", (1 - (1-pA)*(1-pB)));
                 printf("--- c_intersection: %i", c_intersection);
                 printf("--- c_unity: %i", c_unity);
             }*/

             //c_intersection += (*pA++)&&(*pB);
             //c_unity += !(pA++)&&(!(*pB));
             // Fehlt da vielleicht noch eine 2. Verneinung?
          }
          c_fraction = 1 - c_intersection/c_unity;
          // correct the following part later; currently this is just the "trying around" version
          //float threshold = 1.0/m_float;
          //if (c[gid] > threshold*m_float)
          //printf(" gid: %i, c_fraction: %f", gid, c_fraction);

          /*if (c_fraction > threshold)
          {c[gid] = true;}
          else
          {c[gid] = true;}*/
          c[gid] = c_fraction;
        }
        """).build()
    
    prg.multiply(queue, c.shape, None,
                 np.uint16(n), np.uint16(m), np.uint16(p),
                 a_buf, b_buf, c_buf, np.float32(threshold))
    
    a_mul_b = np.empty_like(c)
    cl.enqueue_copy(queue, a_mul_b, c_buf)
    
    if p < n:
        pass
    else:
        result = a_mul_b.reshape(n, p)
        result_transpose = np.transpose(result)
        result_transpose_1d = result_transpose.reshape(n*p, 1).reshape(-1)
        #result_sparse = scipy.sparse.csr_matrix(result)
    
    # info: [1, 2, 2, 2] is an unimportant array, just as a filler in order to build the 
    #     array, the values there have no relevance
    arr = np.array([1, 2, 3, 4], dtype=np.int32)
    adder = gpuadder.GPUAdder(arr)
    if p < n:
        hmat = np.array(a_mul_b, dtype=np.float32)
    else:
        hmat = np.array(result_transpose_1d, dtype=np.float32)

    # info: gpu_l replaced by n and p
    # print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py n: ", n, "; p: ", p)

    if p < n:
        #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: p < n")
        dnnzPerRowColumn_input, dnnzTotalDevHostPtr_input = adder.get_side_indices_caller(hmat, n, p)
        if dnnzTotalDevHostPtr_input > 0:
            idxs, cols, vals = adder.increment(hmat, n, p, dnnzPerRowColumn_input, dnnzTotalDevHostPtr_input[0])
            idxs_normal = make_indices_normal(idxs, control_length=len(cols))
            idxs_total = np.add(idxs_normal, gpu_l*i)
            cols_total = np.add(cols, gpu_l*k)
            vals_total = vals
        else:
            idxs_total = np.array([])
            cols_total = np.array([])
            vals_total = np.array([])

    else:
        # info: hopefully reversing the order of cols and idxs represents a transpos. 
        #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py n < p")
        dnnzPerRowColumn_input, dnnzTotalDevHostPtr_input = adder.get_side_indices_caller(hmat, p, n)
        if dnnzTotalDevHostPtr_input > 0:
            cols, idxs, vals = adder.increment(hmat, p, n, dnnzPerRowColumn_input, dnnzTotalDevHostPtr_input[0])
            idxs_total = np.add(idxs, gpu_l*i)
            cols_normal = make_indices_normal(cols, control_length=len(idxs))
            cols_total = np.add(cols_normal, gpu_l*k)
            vals_total = vals
        else: 
            idxs_total = np.array([])
            cols_total = np.array([])
            vals_total = np.array([])
    #results_sparse.reshape(n, p) - take that correct
        # info: making the indices total: 
    
    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py share of nonzero: ", len(idxs_total)/(n*p))

    # to do: look, how that changes for the two cases in the if-loop above
    """
    idxs_total = np.add(idxs_total, gpu_l*i)
    cols_normal = make_indices_normal(cols, control_length=len(idxs_total))    
    cols_total = np.add(cols_normal, gpu_l*k)
    vals_total = vals
    """

    return (idxs_total, cols_total, vals_total)

def levenshtein_cl_total(strings1, strings2, gpu_l, min_ld, max_ld):
    """
    info: take string arrays and calculate the distance matrix on the GPU;
        Since the string arrays are usually very long, matrix is too big
        to be saved at the GPU at once. Thus it is tiled into parts
    input: strings1: first list of strings
        strings2: second list of strings (usually they are the same)
        gpu_l: sidelength of the tiles in which the 
               matrix is divided for the gpu calculation.
               (the total matrix is too big to save it on the 
               GPU as a hole) (technical value)
        min_ld: minimum threshold for the Levenshtein distance
            to be counted as connected (usually min_ld=0) 
        max_ld: maximum threshold for the Levenshtein distance 
            to be counted as connected
    output: idxs_all: row indices of the nonzero-entries of the sparse
                distance matrix
        cols_all: column indices of the nonzero-entries of the 
            sparse distance matrix
        vals_all: values of the nonzero-entries of the sparse 
            distance matrix
    """
    #todo: If you take min_ld and max_ld as arguments, you should also 
    #    take into account the values of them while performing the GPU calculation 
    
    m = len(strings1)
    n = len(strings2)
    
    # info: old version: m_steps = int(int(m)/gpu_l - int(m%gpu_l)/gpu_l)
    # info: old version: n_steps = int(int(n)/gpu_l - int(n%gpu_l)/gpu_l)
    m_steps = int(int(m)/gpu_l)
    n_steps = int(int(n)/gpu_l)
    max_len = 30
    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: m_steps: ", m_steps, "; n_steps: ", n_steps)
 
    # info: convert the arrays "strings1" and "strings2" into 
    #     arrays of the special ascii type, for more details
    #     see "convert_to_ascii"-function
    ascii_total1, ascii_total2 = convert_to_ascii(strings1, strings2, max_len)

    # info: divide the strings in parts with length gpu_l and 
    #     perform the calculation on the GPU for each tile 
    #     one after the other.
    if m%gpu_l > 0:
        m_steps += 1
    if n%gpu_l > 0:
        n_steps += 1
    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: m_steps: ", m_steps, "; n_steps: ", n_steps)

    #c = scipy.sparse.csr_matrix((n, p), dtype=np.int)
    t0 = time.time()

    idxs_all = np.array([])
    cols_all = np.array([])
    vals_all = np.array([])

    # todo: remove the k loop; that used to be for testing
    #     reasons in order to perform the calculation, but
    #     it is not so necessary anymore.
    for k in range(1):
        #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py k: ", k, "; t: ", time.time()-t0)
        for i in range(m_steps):
            for j in range(n_steps):
                print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py i: \
                        ", i, " / ", m_steps, "; j: ", j, " / ", n_steps)

                # info: calculate the right indices
                if not i == (m_steps-1):
                    m_down = i*gpu_l
                    m_up = (i+1)*gpu_l
                else:
                    m_down = i*gpu_l
                    m_up = n
                
                if not j == (n_steps-1):
                    n_down = j*gpu_l
                    n_up = (j+1)*gpu_l
                
                else:
                    n_down = j*gpu_l
                    n_up = n

                #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py m_down: ", m_down, "; m_up: ", m_up, "; n_down: ", n_down, "; n_up; ", n_up)
                idxs, cols, vals = levenshtein_cl(strings1[m_down:m_up], strings2[n_down:n_up], ascii_total1[(max_len*m_down):(max_len*m_up)], ascii_total2[(max_len*n_down):(max_len*n_up)], max_len, gpu_l, i, j, min_ld, max_ld) 
                #idxs, cols, vals = levenshtein_cl_old(strings1[m_down:m_up], strings2[n_down:n_up], ascii_total1[(max_len*m_down):(max_len*m_up)], ascii_total2[(max_len*n_down):(max_len*n_up)], max_len, gpu_l, i, j, min_ld, max_ld)
                idxs_all = np.concatenate((np.array(idxs_all, dtype=np.int32), np.array(idxs, dtype=np.int32)))
                cols_all = np.concatenate((np.array(cols_all, dtype=np.int32), np.array(cols, dtype=np.int32)))
                vals_all = np.concatenate((np.array(vals_all), np.array(vals)))
                #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py len(vals_all): ", len(vals_all))
    return idxs_all, cols_all, vals_all

def convert_to_ascii(strings1, strings2, max_len):
    """
    info: take two arrays of strings and convert both into 
        the special ascii format, where each character
        is saved as an ubyte (unsigned byte), which is 8 
        bits.
        Actually ASCII would only need 7 bits, so there would
        still be little space for improvement.
        It is assumed, that no string is longer than max_len, which
        is usually 30. If a string is shorter, then "0"-characters
        will be appended until the length is max_len.
        Thus, all strings have the same length, which is 
        necessary in order to define equidistant buffers later
        for the GPU.
        (I think also there is a way to improve that.)
    inputs: strings1: array of strings
        strings2: array of strings
        max_len: maximum length, that each string can have 
        (usually 30)
    outputs: ascii_total1, ascii_total2:
            two string arrays converted to the special ascii_type, where
            each element has the same length max_len
    """
    #ascii_total = np.array([])
    ascii_total = list()
    #strings = strings.astype(np.float32)
    
    for i in range(len(strings1)):
        s = strings1[i] 
        for j in range(len(s), max_len):
            s = s + '0'
        ascii_code = [ord(c) for c in s]
        for j in range(len(ascii_code)):
            ascii_total.append(ascii_code[j])
        #ascii_total = ascii_total + ascii_code
    ascii_total = np.array(ascii_total)
    ascii_total1 = ascii_total.astype(np.ubyte)

    ascii_total = list()
    #strings = strings.astype(np.float32)
    
    for i in range(len(strings2)):
        s = strings2[i]
        for j in range(len(s), max_len):
            s = s + '0'
        ascii_code = [ord(c) for c in s]
        for j in range(len(ascii_code)):
            ascii_total.append(ascii_code[j])
        #ascii_total = ascii_total + ascii_code
    ascii_total = np.array(ascii_total)
    ascii_total2 = ascii_total.astype(np.ubyte)

    return ascii_total1, ascii_total2

def collapse(rows, cols, is_zero, num_blocks, block_size):
    """
    info: remove all empty entries
    input: rows: array of rows
        cols: array of columns
        is_zero: array, saying, if a block is
            zero (is_zero=True) or false;
            if the block is zero, it will be
            skipped
        num_blocks: number of workgroups
        block_size: expected max number of findings
            per workgroup
    output: rows_new: reduced array of columns
        cols_new: array of columns
    """
    rows_new = list()
    cols_new = list()

    i = 0
    while i < num_blocks:
        #if i%10000 == 0:
        #    print("\n in collapse(): i: ", i)
        if is_zero[i] == 0:
            j = 0
            while j < block_size:
                index = i*block_size + j
                if not (rows[index] == -1 and cols[index] == -1):
                    rows_new.append(rows[index])
                    cols_new.append(cols[index])
                j+=1
        i += 1
    """
    for i in range(len(rows)):
        if i%1000 == 0:
            print("\n i: ", i)
        if not (rows[i] == -1 and cols[i] == -1):
            rows_new.append(rows[i])
            cols_new.append(cols[i])
    """

    return rows_new, cols_new

def levenshtein_cl(strings1, strings2, ascii_total1, ascii_total2, max_len, gpu_l, i_index, j_index, min_ld, max_ld):
    """
    info: calculate the distance matrix of the list of strings 
        "strings" using the levenshtein distance on the GPU by 
        using OpenCL
    input: strings1: first list of strings
        strings2: second list of strings
        ascii_total1: first list of strings converted to the 
            asciiformat with filling 0s via the "convert_to_ascii"-
            function
        ascii_total2: second list of strings converted to the 
            asciiformat with filling 0s via the "convert_to_ascii"-
            function
        max_len: maximum length of a string (in the convert_to_ascii)-
            function the remaining part is filled up with 0s. 
            Usually max_len = 30
        gpu_l: sidelength of the tiles in which the 
               matrix is divided for the gpu calculation.
               (the total matrix is too big to save it on the 
               GPU as a hole) (technical value)
        i_index: row index of the matrix block in the matrix
        j_index: column index of the matrix block in the matrix
        min_ld: minimum threshold for the Levenshtein distance
            to be counted as connected (usually min_ld=0)
        max_ld: maximum threshold for the Levenshtein distance
            to be counted as connected
    output: distance matrix 
    """

    # TODO: discard the diagonal terms
    """
    nvmlInit()
    for i in range(nvmlDeviceGetCount()):
        handle = nvmlDeviceGetHandleByIndex(i)
        meminfo = nvmlDeviceGetMemoryInfo(handle)
        print("%s: %0.1f MB free, %0.1f MB used, %0.1f MB total" % (
            nvmlDeviceGetName(handle),
            meminfo.free/1024.**2, meminfo.used/1024.**2, meminfo.total/1024.**2))
    nvmlShutdown()
    """

    print("\n len(strings1): ", len(strings1))

    # info: make zero arrays:
    #     c: array, that contains the results as a matrix
    #     dnew, dprev: technical arrays, only used as intermediate
    #         results during the gpu calculation of the levenshtein 
    #         distance
    
    # TODO: What's a good length? "len(strings1)" is just a rough estimate.
    
    #info: setting for gpu_l = 8000: 
    num_work_groups_estimate = 256000
    
    # info: setting for gpu_l = 40000:
    #num_work_groups_estimate = 6250000 # update that

    max_findings_per_group = 5
    
    len_val = num_work_groups_estimate * max_findings_per_group
    rows = np.zeros(len_val, dtype=np.int32)
    cols = np.zeros(len_val, dtype=np.int32)
    vals = np.zeros(len_val, dtype=np.int32)
    is_zero = np.zeros(num_work_groups_estimate, dtype=np.bool)

    # TODO: What's a good value here?:
    estimated_work_group_num = 10**6

    dnew = np.zeros((len(strings1)), dtype=np.byte)
    dprev = np.zeros((len(strings1)), dtype=np.byte)
    total_count = np.zeros(estimated_work_group_num, dtype=np.int32)

    error1 = np.zeros(3, dtype=np.int32)
    error2 = np.zeros(1, dtype=np.bool)
    groups_id_too_much = np.zeros(1, dtype=np.int32)

    # info: get the GPU and the platform, make command queue, technical
    #     stuff
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags

    # info: make buffers with the two string arrays in the special 
    #     ascii-format (ascii_total1, ascii_total2)
    strings1_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ascii_total1)
    strings2_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ascii_total2)
    
    # info: define ascii code for the above defined arrays c, dnew and dprev
    rows_buf = cl.Buffer(ctx, mf.WRITE_ONLY, rows.nbytes)
    cols_buf = cl.Buffer(ctx, mf.WRITE_ONLY, cols.nbytes)
    #vals_buf = cl.Buffer(ctx, mf.WRITE_ONLY, vals.nbytes)
    total_count_buf = cl.Buffer(ctx, mf.READ_WRITE, total_count.nbytes)
    
    error1_buf = cl.Buffer(ctx, mf.READ_WRITE, error1.nbytes);

    #dnew_buf = cl.Buffer(ctx, mf.WRITE_ONLY, dnew.nbytes)
    #dprev_buf = cl.Buffer(ctx, mf.WRITE_ONLY, dprev.nbytes)
    dnew_buf = cl.Buffer(ctx, mf.READ_WRITE, dnew.nbytes)
    dprev_buf = cl.Buffer(ctx, mf.WRITE_ONLY, dprev.nbytes)
    error1_buf = cl.Buffer(ctx, mf.READ_WRITE, error1.nbytes)
    error2_buf = cl.Buffer(ctx, mf.READ_WRITE, error2.nbytes)
    groups_id_too_much_buf = cl.Buffer(ctx, mf.READ_WRITE, groups_id_too_much.nbytes)
    is_zero_buf = cl.Buffer(ctx, mf.READ_WRITE, is_zero.nbytes) 
    
    """
    nvmlInit()
    for i in range(nvmlDeviceGetCount()):
        handle = nvmlDeviceGetHandleByIndex(i)
        meminfo = nvmlDeviceGetMemoryInfo(handle)
        print("%s: %0.1f MB free, %0.1f MB used, %0.1f MB total" % (
            nvmlDeviceGetName(handle),
            meminfo.free/1024.**2, meminfo.used/1024.**2, meminfo.total/1024.**2))
    nvmlShutdown()
    """
    # info: code for the GPU calculation, written in OpenCL (close to C++);
    #     task of the code: calculate the levenshtein distance
    prg = cl.Program(ctx, """
        __kernel void multiply(__global uchar *strings1, __global uchar *strings2, __global int *global_rows, __global int *global_cols, ushort strings_length1, ushort strings_length2, const ushort max_len, short min_ld, short max_ld, int num_work_groups_estimate, int max_findings_per_group, __global bool *is_zero, __global int *error1)
        { 
        // info: strings_length is the number of strings, NOT the number of letters 
        
        int gid = get_global_id(0);

        if (gid==0)
        {
            for (int i = 0; i<num_work_groups_estimate*max_findings_per_group; i++)
            {
                global_rows[i] = -1;
                global_cols[i] = -1;
            }
        }
        
        int gid1 = get_global_id(0)/strings_length1;
        int gid2 = get_global_id(0)%strings_length2;
        
        int ls = 0;
        int lt = 0;

        bool c_value = 0;

        //#define GL_GPU_MEM_INFO_TOTAL_AVAILABLE_MEM_NVX 0x9048
        //#define GL_GPU_MEM_INFO_CURRENT_AVAILABLE_MEM_NVX 0x9049
       
        // info: find the lengths ls and lt:

        // ----------------------------------------------------------------------------

        //const int max_len_here = 30;
        //#define MYVAL = 30
        char dnew_local[30]; // TODO: replace 30 with constant max_len
        char dprev_local[30];
        char substitutionCost = -1; 
        
        // ----------------------------------------------------------------------------
        
        for (int i = 0; i<max_len; i++)
        {
            if (ls == 0)
            {
                //if (s_pre[i] == (ushort)48) // info: 48 is the ASCII number of '0'
                if (strings1[max_len*gid1 + i] == (ushort)48)
                {
                    ls = i;
                }
            }
            if (lt == 0)
            {
                //if (t_pre[i] == (ushort)48)
                if (strings2[max_len*gid2 + i] == (ushort)48)
                {
                    lt = i;
                }
            }
            // remove 0, that are coded in ASCII code
        }
         
        uint m = ls + 1; //sizeof((uint*)s)/sizeof(uint);
        uint n = lt + 1;

        for (int i = 0; i < m; i++)
        {
            dprev_local[i] = i;
        } 

        for (int j = 1; j < n; j++)
        { 
            dprev_local[0] = j - 1;
            dnew_local[0] = j;
            
            uchar strings2j = strings2[max_len*gid2 + j - 1];
            for (int i = 1; i < m; i++)
            {
                if (strings1[max_len*gid1 + i - 1] == strings2j)
                {
                    substitutionCost = 0;
                }
                else
                {
                    substitutionCost = 1;
                }
                char el1 = dnew_local[i-1] + 1;
                char el2 = dprev_local[i] + 1;
                char el3 = dprev_local[i-1] + substitutionCost;
                
                // info: a very tricky smart way to find the min:
                
                //(el1 > el2) && (el1 = el2);
                //(el1 > el3) && (el1 = el3);    
                //dnew_local[i] = el1;
            
                char chosen;
                if (el1 < el2)
                {
                    chosen = el1;
                }
                else
                {
                    chosen = el2;
                }
                if (el3 < chosen)
                {
                    chosen = el3;
                }
                dnew_local[i] = chosen;
            }
            
            for (int i = 1; i < m; i++)
            {
                dprev_local[i] = dnew_local[i];
            }
        }
        
        // ------------------------- C Value part -------------------------------------

        // info: c is 1, if the distance min_ld and max_ld,
        //     0 otherwise

        //printf("\\n gid: %i, dnew_local[m-1]: %i, gid1: %i, gid2: %i", gid, dnew_local[m-1], gid1, gid2);
        
        if ((short) dnew_local[m-1] < max_ld)
        {
            if ((short) dnew_local[m-1] > min_ld)
            {
                c_value = 1;
            }
        }
        else
        {
            c_value = 0;
        }
        
        // info: try to implement the direct sparse:
        int lid = get_local_id(0);
        int lsz = get_local_size(0);
        
        // TODO: Replace 1000 by a useful number
        // default value: 5:
        __local int local_rows[5];
        __local int local_cols[5];
        __local int count;
        
        int local_rows_len = sizeof(local_rows)/sizeof(local_rows[0]);

        count = 0;
    
        for (int i=0; i < lsz; i++)
        {
            if (lid == i)
            {
                if (c_value != 0)
                {
                    // pay attention, that because of transposing, rows and cols are not confused
                    // /-*if (count > local_rows_len)
                    // {
                    //    error1[0] = 1;
                    // }*-/
                    local_rows[count] = gid/strings_length2;
                    local_cols[count] = gid%strings_length2;
                    count += 1;
                }
            }
            barrier(CLK_LOCAL_MEM_FENCE);
        }
        barrier(CLK_GLOBAL_MEM_FENCE);
        
        int group_id = get_group_id(0);
        int groups_num = get_num_groups(0);
        
        if (lid == 0)
        {
            if (count == 0)
            {
                is_zero[group_id] = 1;
            }
            if (count > max_findings_per_group)
            {
                error1[0] = 1;
                error1[1] = count;
                error1[2] = max_findings_per_group;
            }
        }
    
        if (gid == 0)
        {
            printf("\\n get_local_size: %i", lsz);
            printf("\\n groups_num: %i", groups_num);
            if (error1[0] == 1)
            {
                printf("\\n There seems to be an error: ");
                printf("\\n count > max_findings_per_group");
                printf("\\n count: %i", error1[1]);
                printf("\\n max_findings_per_group: %i", error1[2]);
            }
        }
        
        if (lid < count)
        {
            //printf("\\n max_findings_per_group*group_id + lid: %i, global_rows: %i", (max_findings_per_group*group_id + lid), (global_rows[max_findings_per_group*group_id + lid]));
            global_rows[max_findings_per_group*group_id + lid] = local_rows[lid];
            global_cols[max_findings_per_group*group_id + lid] = local_cols[lid];
        }
        }
        """ ).build()
   
    # info: execute the above OpenCL code on the GPU
    #completeEvent = prg.multiply(queue,  (len(strings1)*len(strings2),), None, strings1_buf)
    completeEvent = prg.multiply(queue, (len(strings1)*len(strings2),), None, strings1_buf, strings2_buf, rows_buf, cols_buf, np.uint16(len(strings1)), np.uint16(len(strings2)), np.uint16(max_len), np.short(min_ld), np.short(max_ld), np.int32(num_work_groups_estimate), np.int32(max_findings_per_group), is_zero_buf, error1_buf)
    events = [ completeEvent ];

    rows = np.empty_like(rows)
    cols = np.empty_like(cols)
    vals = np.empty_like(vals)
    is_zero = np.empty_like(is_zero)

    cl.enqueue_copy(queue, rows, rows_buf, wait_for=events);
    cl.enqueue_copy(queue, cols, cols_buf, wait_for=events);
    cl.enqueue_copy(queue, is_zero, is_zero_buf, wait_for=events);
    #cl.enqueue_copy(queue, vals, vals_buf, wait_for=events);
    #print("\n before rows: ", list(rows), "; cols: ", list(cols), "; vals: ", list(vals))    
    rows, cols = collapse(rows, cols, is_zero, num_work_groups_estimate, max_findings_per_group)

    rows = np.add(rows, i_index*gpu_l)
    cols = np.add(cols, j_index*gpu_l)

    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: len(rows): ", len(list(rows)), "; len(cols): ", len(list(cols)), "; len(vals): ", len(list(vals)))
    """
    print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: strings1: ", strings1, "; strings2: ", strings2)
    """
    #print("\n after rows: ", list(rows), "; cols: ", list(cols), "; vals: ", list(vals))
    return rows, cols, vals

def levenshtein_cl_old(strings1, strings2, ascii_total1, ascii_total2, max_len, gpu_l, i_index, j_index, min_ld, max_ld):
    """
    info: calculate the distance matrix of the list of strings 
        "strings" using the levenshtein distance on the GPU by 
        using OpenCL
    input: strings1: first list of strings
        strings2: second list of strings
        ascii_total1: first list of strings converted to the 
            asciiformat with filling 0s via the "convert_to_ascii"-
            function
        ascii_total2: second list of strings converted to the 
            asciiformat with filling 0s via the "convert_to_ascii"-
            function
        max_len: maximum length of a string (in the convert_to_ascii)-
            function the remaining part is filled up with 0s. 
            Usually max_len = 30
        gpu_l: sidelength of the tiles in which the 
               matrix is divided for the gpu calculation.
               (the total matrix is too big to save it on the 
               GPU as a hole) (technical value)
        i_index: row index of the matrix block in the matrix
        j_index: column index of the matrix block in the matrix
        min_ld: minimum threshold for the Levenshtein distance
            to be counted as connected (usually min_ld=0)
        max_ld: maximum threshold for the Levenshtein distance
            to be counted as connected
    output: distance matrix 
    """

    # TODO: discard the diagonal terms

    nvmlInit()
    for i in range(nvmlDeviceGetCount()):
        handle = nvmlDeviceGetHandleByIndex(i)
        meminfo = nvmlDeviceGetMemoryInfo(handle)
        print("%s: %0.1f MB free, %0.1f MB used, %0.1f MB total" % (
            nvmlDeviceGetName(handle),
            meminfo.free/1024.**2, meminfo.used/1024.**2, meminfo.total/1024.**2))
    nvmlShutdown()

    print("\n len(strings1): ", len(strings1))

    # info: make zero arrays:
    #     c: array, that contains the results as a matrix
    #     dnew, dprev: technical arrays, only used as intermediate
    #         results during the gpu calculation of the levenshtein 
    #         distance
    
    # TODO: What's a good length? "len(strings1)" is just a rough estimate.
    
    """
    #info: setting for gpu_l = 8000: 
    num_work_groups_estimate = 256000
    
    # info: setting for gpu_l = 40000:
    #num_work_groups_estimate = 6250000 # update that

    max_findings_per_group = 5
    
    len_val = num_work_groups_estimate * max_findings_per_group
    rows = np.zeros(len_val, dtype=np.int32)
    cols = np.zeros(len_val, dtype=np.int32)
    vals = np.zeros(len_val, dtype=np.int32)
    is_zero = np.zeros(num_work_groups_estimate, dtype=np.bool)
    
    # TODO: What's a good value here?:
    estimated_work_group_num = 10**6
    
    distance = np.zeros()
    """
    dnew = np.zeros((len(strings1)), dtype=np.byte)
    dprev = np.zeros((len(strings1)), dtype=np.byte)
    """
    total_count = np.zeros(estimated_work_group_num, dtype=np.int32)
    """
    is_zero = np.zeros(len(strings1)*len(strings2), dtype=np.bool)

    """
    error1 = np.zeros(3, dtype=np.int32)
    error2 = np.zeros(1, dtype=np.bool)
    groups_id_too_much = np.zeros(1, dtype=np.int32)
    """

    # info: get the GPU and the platform, make command queue, technical
    #     stuff
    platform = cl.get_platforms()
    my_gpu_devices = platform[0].get_devices(device_type=cl.device_type.GPU)
    ctx = cl.Context(devices=my_gpu_devices)
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags

    # info: make buffers with the two string arrays in the special 
    #     ascii-format (ascii_total1, ascii_total2)
    is_zero_buf = cl.Buffer\
        (ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=is_zero)
    
    strings1_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ascii_total1)
    strings2_buf = cl.Buffer\
        (ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=ascii_total2)
    """
    # info: define ascii code for the above defined arrays c, dnew and dprev
    rows_buf = cl.Buffer(ctx, mf.WRITE_ONLY, rows.nbytes)
    cols_buf = cl.Buffer(ctx, mf.WRITE_ONLY, cols.nbytes)    
    #vals_buf = cl.Buffer(ctx, mf.WRITE_ONLY, vals.nbytes)
    #total_count_buf = cl.Buffer(ctx, mf.READ_WRITE, total_count.nbytes)
    error1_buf = cl.Buffer(ctx, mf.READ_WRITE, error1.nbytes);
    """
    nvmlInit()

    #     task of the code: calculate the levenshtein distance
    prg = cl.Program(ctx, """
        __kernel void multiply(__global uchar *strings1, __global uchar *strings2, ushort strings_length1, ushort strings_length2, const ushort max_len, short min_ld, short max_ld, __global bool *is_zero)
        { 
        // info: strings_length is the number of strings, NOT the number of letters 
        
        int gid = get_global_id(0);
        /*
        if (gid==0)
        {
            // find total size
            for (int i = 0; i<total_size; i++)
            {
                global_rows[i] = -1;
                global_cols[i] = -1;
            }
        }*/
        
        int gid1 = get_global_id(0)/strings_length1;
        int gid2 = get_global_id(0)%strings_length2;
        
        int ls = 0;
        int lt = 0;

        bool c_value = 0;

        //#define GL_GPU_MEM_INFO_TOTAL_AVAILABLE_MEM_NVX 0x9048
        //#define GL_GPU_MEM_INFO_CURRENT_AVAILABLE_MEM_NVX 0x9049
       
        // info: find the lengths ls and lt:

        // ----------------------------------------------------------------------------

        //const int max_len_here = 30;
        //#define MYVAL = 30
        char dnew_local[30]; // TODO: replace 30 with constant max_len
        char dprev_local[30];
        char substitutionCost = -1; 
        
        // ----------------------------------------------------------------------------
        
        for (int i = 0; i<max_len; i++)
        {
            if (ls == 0)
            {
                //if (s_pre[i] == (ushort)48) // info: 48 is the ASCII number of '0'
                if (strings1[max_len*gid1 + i] == (ushort)48)
                {
                    ls = i;
                }
            }
            if (lt == 0)
            {
                //if (t_pre[i] == (ushort)48)
                if (strings2[max_len*gid2 + i] == (ushort)48)
                {
                    lt = i;
                }
            }
            // remove 0, that are coded in ASCII code
        }
         
        uint m = ls + 1; //sizeof((uint*)s)/sizeof(uint);
        uint n = lt + 1;

        for (int i = 0; i < m; i++)
        {
            dprev_local[i] = i;
        } 

        for (int j = 1; j < n; j++)
        { 
            dprev_local[0] = j - 1;
            dnew_local[0] = j;
            
            uchar strings2j = strings2[max_len*gid2 + j - 1];
            for (int i = 1; i < m; i++)
            {
                if (strings1[max_len*gid1 + i - 1] == strings2j)
                {
                    substitutionCost = 0;
                }
                else
                {
                    substitutionCost = 1;
                }
                char el1 = dnew_local[i-1] + 1;
                char el2 = dprev_local[i] + 1;
                char el3 = dprev_local[i-1] + substitutionCost;
                
                // info: a very tricky smart way to find the min:
                
                //(el1 > el2) && (el1 = el2);
                //(el1 > el3) && (el1 = el3);    
                //dnew_local[i] = el1;
            
                char chosen;
                if (el1 < el2)
                {
                    chosen = el1;
                }
                else
                {
                    chosen = el2;
                }
                if (el3 < chosen)
                {
                    chosen = el3;
                }
                dnew_local[i] = chosen;
            }
            
            for (int i = 1; i < m; i++)
            {
                dprev_local[i] = dnew_local[i];
            }
        }
        
        if ((short) dnew_local[m-1] < max_ld)
        {
            if ((short) dnew_local[m-1] > min_ld)
            {
                c_value = 1;
            }
        }
        else
        {
            c_value = 0;
        }
        
        is_zero[gid] = c_value;
        }
        """ ).build()
   
    # info: execute the above OpenCL code on the GPU
    #completeEvent = prg.multiply(queue,  (len(strings1)*len(strings2),), None, strings1_buf)
    completeEvent = prg.multiply(queue, (len(strings1)*len(strings2),), None, strings1_buf, strings2_buf, np.uint16(len(strings1)), np.uint16(len(strings2)), np.uint16(max_len), np.short(min_ld), np.short(max_ld), is_zero_buf)

    events = [ completeEvent ];
    """
    rows = np.empty_like(rows)
    cols = np.empty_like(cols)
    vals = np.empty_like(vals)
    """
    is_zero = np.empty_like(is_zero)

    """
    cl.enqueue_copy(queue, rows, rows_buf, wait_for=events);
    cl.enqueue_copy(queue, cols, cols_buf, wait_for=events);
    """
    cl.enqueue_copy(queue, is_zero, is_zero_buf, wait_for=events);
    #cl.enqueue_copy(queue, vals, vals_buf, wait_for=events);
    #print("\n before rows: ", list(rows), "; cols: ", list(cols), "; vals: ", list(vals))    
    """
    rows, cols = collapse(rows, cols, is_zero, num_work_groups_estimate, max_findings_per_group)

    rows = np.add(rows, i_index*gpu_l)
    cols = np.add(cols, j_index*gpu_l)
    """
    #print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: len(rows): ", len(list(rows)), "; len(cols): ", len(list(cols)), "; len(vals): ", len(list(vals)))
    """
    print("\n /home/paul/Documents/imnet-master2/opencl_matrix.py: strings1: ", strings1, "; strings2: ", strings2)
    """
    #print("\n after rows: ", list(rows), "; cols: ", list(cols), "; vals: ", list(vals))
    
    # info: make two lists, which contain the nodes, which are connected
    rows = list()
    cols = list()
    
    len_strings1 = len(strings1)

    for i in range(len(is_zero)):
        print("\n i: ", i, " / ", len(is_zero))
        # does is_zero have to be true or false?
        if is_zero[i] == False:
            rows.append(int(i/len_strings1))
            cols.append(int(i%len_strings1))

    return rows, cols, is_zero
    #return rows, cols, vals

"""
t zellen bleiben
formel in den appendix
vdj weniger detailliert
paper sektion 6.5 -> diversity also

epfl

informatik:
hofmann, bufmann, krause
"""



