__all__ = [
    "stripe_removal",
    "stripe_del",
    "xRemoveSpriesHorizontal",
    "image_flattening",
    "gaussian_flattening",
    "poly_flattening",
    "analyse_morphologique",
    "read_image",
]



def stripe_removal(ima, **kwargs):

    """
    Stripes removal from an image.

    Arguments :
        ima (nparray): image to process
        **kwargs: kwargs["method"] = "wavelet" or "epandage" (default "wavelet")
                  kwargs["mode"] = "mean", "median", "mode", "poly" (default "median")
                  kwargs["order"]  order orde of the smoothing polynomial
                  kwargs["wname"] wname of the wavelet (default db15)
                  kwargs["decNum_h"] order of decimation
                  kwargs["sigma_wl_h"] sigma_wl_h
    Returns:
        iama: corrected image
    """

    if "method" in list(kwargs.keys()):
        method_type = kwargs["method"]
    else:
        method_type = "wavelet"

    if method_type == "epandage":
        try:
            mode = kwargs["mode"]
        except:
            mode = "median"

        if mode == 'poly':
            try:
                order = kwargs["order"]
            except:
                order = 3
            ima = stripe_del(ima, mode, order)
        else:
            ima = stripe_del(ima, mode)

    elif method_type == "wavelet":
        try:
            wname = kwargs["wname"]
        except:
            wname = "db15"

        try:
            decNum_h = kwargs["decNum_h"]
        except:
            decNum_h = 7

        try:
            sigma_wl_h = kwargs["sigma_wl_h"]
        except:
            sigma_wl_h = 3

        ima = xRemoveSpriesHorizontal(ima,decNum_h,wname,sigma_wl_h)

    else:
        raise Exception(f"unknown method:{method_type}")

    return ima




def stripe_del(ima, mode, order=3):
    '''Supress stripe by aligning row using different method
    median: for each row, subtract the row median value from that row
    mean: for each row, subtract the row mean value from that row
    mode: for each row, subtract the mode value from that row
    polynomial: for each row, subtract least square smoothing polynomial from that row

    Arguments
        ima (nparray): image to process
        mode (string): algorith to apply (mean, median, mode, polynomial)
        order (integer): order of the smoothing polynomial
    Returns
        ima (nparray): corrected image
    '''
    # 3rd party import
    import numpy as np
    from scipy import stats
    import pandas as pd

    if mode=='median':
        epandage = np.median(ima,axis=1).reshape((np.shape(ima)[0] ,1))
        ima = ima - epandage

    elif mode=='mean':
        epandage = np.mean(ima,axis=1).reshape((np.shape(ima)[0] ,1))
        ima = ima - epandage

    elif mode == 'mode':
        epandage = stats.mode(ima,axis=1)[0].flatten().reshape((np.shape(ima)[0] ,1))
        ima = ima - epandage

    elif mode == 'poly':
        df = pd.DataFrame(ima)
        imb = []
        for row in df.iterrows():
            coeff = np.polyfit(np.array(row[1].index), np.array(row[1].values), order)
            imb.append(np.array(row[1].values) - np.polyval(coeff, np.array(row[1].index)))
        ima = np.array(imb).reshape(np.shape(ima))

    return ima

def xRemoveSpriesHorizontal(ima,decNum,wname,sigma):

    '''
    Horizontal stripes supression using the folowing algorithm
    [1] https://www.osapublishing.org/oe/abstract.cfm?uri=oe-17-10-8567

    Arguments:
        ima (ndarray) : image to process
        decNum (integer) : decimation number
        wname (string) : wavelet type
        sigma (float): damping factor (see [1])
    Returns:
        imc (ndarray) : filtered image

    '''
    # 3rd party import
    import numpy.matlib
    import numpy as np
    import pywt

    # wavelet decomposition
    coeffs = pywt.wavedec2(ima, wname, level=decNum)
    ima=coeffs[0]
    cH=[coeffs[I][0] for I in range(1,decNum+1)]
    cV=[coeffs[I][1] for I in range(1,decNum+1)]
    cD=[coeffs[I][2] for I in range(1,decNum+1)]

    # FFT transform of horizontal frequency bands
    cHf=[]
    for cH_ in cH:
        fcH=np.fft.fftshift(np.fft.fft(cH_))
        [my,mx]=np.shape(fcH)

        # damping of vertical strips information
        m=mx
        damp=1-np.exp(-np.arange(np.floor(-m/2),np.floor(-m/2)+m)*np.arange(np.floor(-m/2),np.floor(-m/2)+m)/(2*np.power(sigma,2)))
        fcH=fcH*(np.matlib.repmat(damp,my,1))
        # inverse FFT
        cHf.append(np.fft.ifft(np.fft.ifftshift(fcH)))


    coefft=[ima]
    for ii in range(decNum):
        coefft.append((cHf[ii],cV[ii],cD[ii]))

    imc=pywt.waverec2(coefft, wname)
    imc = np.real(imc)
    imc = imc - imc.min()
    return imc

def image_flattening(ima, **kwargs):

    """
    Stripes removal from an image.

    Arguments :
        ima (nparray): image to process
        **kwargs: kwargs["method_flat"]
                  kwargs["sigma"]
                  kwargs["kx"]
                  kwargs["ky"]


    Returns:
        ima (nparray): corrected image
    """
    if "method_flat" in list(kwargs.keys()):
        method_type = kwargs["method_flat"]
    else:
        method_type = "gauss"

    if method_type == "gauss":
        try:
            sigma = kwargs["sigma"]
        except:
            sigma = 3
        ima = gaussian_flattening(ima, sigma)

    elif method_type == "poly":
        try:
            kx = kwargs["kx"]
        except:
            sigma = 2

        try:
            ky = kwargs["ky"]
        except:
            ky = 2
        ima = poly_flattening(ima, kx, ky, order=None)

    else:
        raise Exception(f"unknown method:{method_type}")

    return ima



def gaussian_flattening(im, sigma):

    '''
    Image flattening
    '''
    # 3rd party imports
    from scipy.ndimage import gaussian_filter

    im_flat = im/gaussian_filter(im, sigma=sigma)
    return im_flat

def poly_flattening(im, kx, ky, order=None):

    # 3rd party imports
    import numpy as np

    ny,nx = np.shape(im)
    x = np.arange(0,nx,1)/nx
    y = np.arange(0,ny,1)/ny

    coeff = polyfit2d(x,y, im, kx=kx, ky=ky, order = order)
    im_background = poly2Dreco(x,y,coeff)
    im_flatten = im - im_background

    return im_flatten

def polyfit2d(x, y, z, kx, ky, order):

    '''
    Two dimensional polynomial fitting by least squares.
    Fits the functional form f(x,y) = z.
    credit : https://stackoverflow.com/questions/33964913/equivalent-of-polyfit-for-a-2d-polynomial-in-python


    Arguments
        x, y (array-like, 1d) : x and y coordinates.
        z (np.ndarray, 2d) : Surface to fit.
        kx, ky (int, default is 3) : Polynomial order in x and y, respectively.
        order (int or None, default is None) :
            If None, all coefficients up to maxiumum kx, ky, ie. up to and including x^kx*y^ky, are considered.
            If int, coefficients up to a maximum of kx+ky <= order are considered.

    Returns
        coeff (np.ndarray, 2d): polynomial coefficients c(i,j) y**i x**j

    '''

    # 3rd party imports
    import numpy as np

    x, y = np.meshgrid(x, y)
    coeffs = np.ones((kx+1, ky+1))
    a = np.zeros((coeffs.size, x.size))

    for index, (i,j) in enumerate(np.ndindex(coeffs.shape)):
        # do not include powers greater than order
        if order is not None and i + j > order:
            arr = np.zeros_like(x)
        else:
            arr = coeffs[i, j] * x**i * y**j
        a[index] = arr.ravel()

    coeff, _, _, _ = np.linalg.lstsq(a.T, np.ravel(z), rcond=None)
    return coeff.reshape(kx+1,ky+1)

def poly2Dreco(x,y, c):
    import numpy as np
    return np.polynomial.polynomial.polygrid2d(x,y,c).T


def analyse_morphologique(img):

    '''
    find the features in the image
    Arguments:
        img (ndarray): image to analyze
        path (string): absolute path of the excel file containing the dataframe df (see returns)
                       optional (default=None no storage)
    Returns:
        df (dataframe): index|'x'|'long_x'| 'y'|'long_y'| 'size'
    '''

    import numpy as np
    from scipy.ndimage.measurements import label
    import pandas as pd

    labeled_array, num_features = label(img,[[0,1,0], [1,1,1], [0,1,0]])

    morpho = {}

    for i in range(1,np.max(labeled_array)+1):
        x,y = np.where(labeled_array==i)
        morpho[i] = [ int(np.mean(x)), max(x)-min(x)+1, int(np.mean(y)), max(y)-min(y)+1, np.sum(labeled_array==i)]

    df = pd.DataFrame.from_dict(morpho, orient='index',
                           columns=['x','long_x', 'y','long_y', 'size'])

    return df

def Otsu_tresholding(im,Ostu_corr=1):
    '''
    Image thresholding using the Otsu's method
    https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4310076
    Arguments:
        im (ndarray) : image
        Ostu_corr (float) : division of the Otsu threshold by Otsu_corr

    Returns:
        im_bin (ndarray) : binarized image
    '''

    from skimage import filters
    import numpy as np

    thresh_otsu = filters.threshold_otsu(convert(im)) # détermination du seuil optimum selon Otsu
    im_bin = np.where((convert(im) < thresh_otsu/Ostu_corr), 1, 0)
    return im_bin

def top_hat_flattening(im,struct_elmt_size):
    ''' mise à plat de l image en appliquant une transformation top hat à chacune des lignes de l image im'''
    from scipy.ndimage import white_tophat
    (mx,my)=np.shape(im)
    Ip=[]
    for ii in range(mx):
        Ip.append(white_tophat(im[ii,:], None, np.repeat([1], struct_elmt_size)))
    Ip=np.array(Ip).reshape((mx,my))
    Ip=255*Ip/np.max(np.max(Ip))

    return Ip


def effective_erea(df,n_row, n_col):
    surf = lambda size_min: 100*df.query("size > @size_min")["size"].sum()/(n_row* n_col)
    eff_erea = [surf(size_min) for size_min in range(max(df["size"])+1)]
    return eff_erea

def convert(data):
    import numpy as np
    data = data / data.max() #normalizes data in range 0 - 255
    data = 255 * data
    return data.astype(np.uint8)

def read_image(file):
    import numpy as np
    import matplotlib.pyplot as plt

    img = plt.imread(file, 1)
    im_brute=img[:,:,0]
    n_row, n_col,_ = np.shape(img)
    return im_brute,n_row, n_col

def image_processing(param,analyse_morpho=True):

    from pathlib import Path
    # lecture de l'image
    im_brute,n_row, n_col = read_image(param['repertoire'] / param['file'])

    # mise à plat de l'image
    im_flat = gaussian_flattening(im_brute, sigma=param['sigma'])
    #im_flat = poly_flattening(im_brute)

    # supression des traces verticales
    im_corr_strie = xRemoveSpriesHorizontal(im_flat,param['decNum_h'],param['wname'],param['sigma_wl_h'])


    # binarisation de l'image
    im_bin = Otsu_tresholding(im_corr_strie,Ostu_corr=param['Ostu_corr'])

    # analyse morphologique
    df= None
    if analyse_morpho:
        file_save_excel = Path(param['file']).stem +'.xlsx'
        df = analyse_morphologique(im_bin)
        df.to_excel(param['dir_results']/file_save_excel)
    return im_brute, im_corr_strie, im_flat, im_bin, df


def make_tex_document(param, im_brute, im_corr_strie, im_flat, im_bin, df, mode='w',flag=False,new_section=False):

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    from pathlib import Path
    import os

    size_min = 50
    alpha1 = 0.35
    alpha2 = 0.8

    print(param['file'])
    n_row, n_col = np.shape(im_brute)

    fig = plt.figure(figsize=(8,8))
    ax1= fig.add_subplot(111)
    im_flat = im_flat - im_flat.min()
    ax1.imshow(im_flat,interpolation="nearest", cmap=plt.cm.gray)

    df1 = df.query("size >= @size_min")
    patchesb = []
    for x1,y1,r in zip(df1['y'],df1['x'],df1['size']):
        circle = plt.Circle((x1,y1), np.sqrt(r/np.pi))
        patchesb.append(circle)

    df1 = df.query("size < @size_min")
    patchesc = []
    for x1,y1,r in zip(df1['y'],df1['x'],df1['size']):
        circle = plt.Circle((x1,y1), np.sqrt(r/np.pi))
        patchesc.append(circle)

    p = matplotlib.collections.PatchCollection(patchesb, cmap=matplotlib.cm.jet, alpha=alpha1, facecolor="blue")
    pc = matplotlib.collections.PatchCollection(patchesc, cmap=matplotlib.cm.jet, alpha=alpha2, facecolor="green")
    ax1.add_collection(p)
    ax1.add_collection(pc)
    file_save_im_brute = Path(param['file']).stem +'-im-brute.jpg'
    plt.savefig(param['dir_results']/file_save_im_brute, bbox_inches='tight')
    plt.close(fig)

    fig = plt.figure(figsize=(8,8))
    ax1= fig.add_subplot(111)
    ax1.imshow(convert(im_bin),interpolation="nearest", cmap=plt.cm.gray)
    file_save_im_bin = Path(param['file']).stem +'-im-bin.jpg'
    plt.savefig(param['dir_results']/file_save_im_bin, bbox_inches='tight')
    plt.close(fig)

    fig = plt.figure(figsize=(8,8))
    ax1= fig.add_subplot(111)
    ax1.hist(df['size'] ,bins=40)
    ax1.set_title("histogramme des tailles")
    file_save_im_hist = Path(param['file']).stem +'-im-hist.jpg'
    plt.savefig(param['dir_results']/file_save_im_hist, bbox_inches='tight')
    plt.close(fig)

    fig = plt.figure(figsize=(8,8))
    ax1= fig.add_subplot(111)
    ax1.boxplot(df['size'])
    file_save_im_erea = Path(param['file']).stem +'-im-bbox.jpg'
    plt.savefig(param['dir_results']/file_save_im_erea, bbox_inches='tight')
    plt.close(fig)

    file_save_doc_tex = Path(param['file']).stem +'_doc_tex.tex'
    with open(param['dir_tex']/Path('rapport.tex'),mode) as doc:
        if mode=='w':
            doc.write(r'''\documentclass[a4paper, 10pt]{article}
        \usepackage[american]{babel}
        \usepackage{amsmath}
        \usepackage{amsthm}
        \numberwithin{equation}{section}
        \usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}
        \usepackage{graphicx}
        \usepackage{hyperref}
        \usepackage{empheq}
        \usepackage{pythonhighlight}''')
            doc.write(r'\graphicspath{'+ ",".join(["{./"+"wafer "+str(i)+"/" +'results}' for i in range(1,6)])+'}')
            doc.write(r'''\begin{document}
        \tableofcontents
        \newpage'''+'\n')
            #doc.write(r'\section{' + str(param['repertoire']).split('\\')[-2]+'}'+'\n')

            doc.write(r'\section{Parameters}')
            doc.write(r"\begin{center} \begin{tabular}{|" + " | ".join(["l"] * 2) + "|}\n")
            doc.write("\\hline\n")
            doc.write(" & ".join([str(x) for x in ['parameter', 'Value']]) + " \\\\\n")
            doc.write("\\hline\n")
            doc.write("\\hline\n")
            for key, value in param.items():
                if key in ['wname','sigma_wl_h','decNum_h','sigma','Ostu_corr']:

                    doc.write( key.replace('_','\_') + " & "  + str(value) + " \\\\\n")
                    doc.write("\\hline\n")
            doc.write(r"\end{tabular} \end{center} ")



            doc.write(r'\section{'+param['coupe']+'}'+'\n')
        if new_section:
            doc.write(r'\subsection{'+param['wafer']+'}'+'\n')
        doc.write(r'\subsubsection{'+param['file']+'}'+'\n')
        doc.write(r'''\begin{figure}[h]
        \begin{center}
        \begin{tabular}{cc}
        (a) & (b)\\'''+'\n')
        doc.write(r'\includegraphics[width=0.5\textwidth]{'+
                  file_save_im_brute+
                  r'} & \includegraphics[width=0.5\textwidth]{'+
                  file_save_im_bin+r'}\\'+'\n')
        doc.write(r'(c) & (d)\\'+'\n')
        doc.write(r'\includegraphics[width=0.5\textwidth]{'+
                  file_save_im_hist+
                  r'} & \includegraphics[width=0.5\textwidth]{'+
                  file_save_im_erea+r'}\\'+'\n')
        doc.write(r'''\end{tabular}
        \end{center}
        \caption{Image processing: (a) Superposition of the flattened image with the detected defaults, the erea of the circles
        are equal to the erea of the defaults, the green circle have an area less than 50 px, the blue one have area greater or
        equal than 50 px
        ; (b) Binarized image; (c) Area histogram; (d) Box plot of the area.}
        \end{figure}'''+'\n')
        if flag:
            build_bbox(param,size_min=0 )
            doc.write(r'\section {Synthese}')
            doc.write(r'\includegraphics[width=0.9\textwidth]{synthesege0.png} \newpage ')
            build_bbox(param,size_min=size_min, method="lt" )
            doc.write(r'\includegraphics[width=0.9\textwidth]{syntheselt'+str(size_min)+ r'.png} \newpage ')
            build_bbox(param,size_min=size_min, method="ge" )
            doc.write(r'\includegraphics[width=0.9\textwidth]{synthesege'+str(size_min)+'.png}')
            doc.write(r'\end {document}')
        else:
            doc.write(r'\newpage')

    return

def build_bbox(param, size_min=50, method="ge"):

    import pandas as pd
    from pathlib import Path

    REP = [param['root'] / Path(param['coupe']) / Path("wafer "+str(i)) /Path('results') for i in range(1,6)]
    s = {}
    len_max = 0
    for rep in REP:
        for x in [y for y in os.listdir(rep) if y.split('.')[-1] == 'xlsx']:
            df = pd.read_excel(rep/x)
            key = x.split('.')[0]
            if method=="ge":
                s[key ] = df.query("size >= @size_min")["size"]
            else:
                s[key ] = df.query("size < @size_min")["size"]

            len_max =max(len(s[key]), len_max)
    for key, value in s.items():
        dif = len_max-len(value)
        if dif > 0:
            a = list(value)
            a.extend([None]*(dif))
            s[key] = a
    df = pd.DataFrame.from_dict(s)

    ax = df.plot.box(rot=0, figsize=(8,15), grid = True, vert=False)
    ax.set_title(coupe)
    plt.savefig(param['root']/Path(param['coupe'])/Path("synthese"+method+str(size_min)+".png"), bbox_inches='tight')
    plt.close(fig)
    return


