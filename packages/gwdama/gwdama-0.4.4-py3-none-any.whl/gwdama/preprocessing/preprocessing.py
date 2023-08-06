"""
This module contains a collection of functions intended for simple data anlysis and preprocessing of the data.
These are basically in continuous grow from the possible use cases in which :ref:`index:gwdama` finds applications. 

Some of these functions are also provided as *methods* for the :ref:`dataset` class.
"""
import numpy as np
import scipy
#from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import get_window, argrelmin, argrelmax, spectrogram, welch, decimate
from multiprocessing import Pool, cpu_count
from functools import partial

def whiten(strain, interp_psd, dt, phase_shift=0, time_shift=0):
    """Function that returns the whitened strain data given the PSD and sample rate, also optionally applying a phase
    shift and time shift.

    Parameters
    ----------
    strain : array_like
        a time series, such as the strain data
    interp_psd : interpolating function
        function to take in freqs and output the average power at that freq 
    dt : float
        sample time interval of data
    phase_shift : float, optional
        phase shift to apply to whitened data
    time_shift : float, optional
        time shift to apply to whitened data (s)
    
    Returns
    -------
    whitened : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Array of whitened strain data
    """
    Nt = len(strain)
    # take the fourier transform of the data
    freqs = np.fft.rfftfreq(Nt, dt)

    # whitening: transform to freq domain, divide by square root of psd, then
    # transform back, taking care to get normalization right.
    hf = np.fft.rfft(strain)
    
    # apply time and phase shift
    hf = hf * np.exp(-1.j * 2 * np.pi * time_shift * freqs - 1.j * phase_shift)
    norm = 1./np.sqrt(1./(dt*2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht

def bandpass(strain, fband, fs):
    """Bandpasses strain data using a butterworth filter.
    
    Args:
        strain (ndarray): strain data to bandpass
        fband (ndarray): low and high-pass filter values to use
        fs (float): sample rate of data
    
    Returns:
        ndarray: array of bandpassed strain data
    """
    from scipy.signal import butter, filtfilt
    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_bp = filtfilt(bb, ab, strain) / normalization
    return strain_bp

def next_power_of_2(x):
    """
    Silly functions to obtain the "next power of 2" for any given
    number ``x``. It is useful for padding before computing the FFTs needed for spectral estimations, such as for the Welch's method.
    This is computed by means of the `bit_length method <https://docs.python.org/3/library/stdtypes.html#int.bit_length>`_ of ints, corresponding to the number of bits necessary to represent an integer in binary, excluding the sign and leading zeros
    
    Parameters
    ----------
    x : int
        Number, for example the length of an array
    Returns
    -------
    n : int
        equals to 1 if ``x==0``, the next power of two of ``x`` otherwise
        
    """   
    return 1 if x == 0 else 2**(x - 1).bit_length()


def taper(data, fs=1, side='leftright', duration=None, nsamples=None, window=('tukey',0.25)):
    """Taper the edges of this datset smoothly to zero. The method automatically tapers from the second stationary point (local maximum or minimum) on the specified side of the input. However, the method will never taper more than half the full width of the data, and will fail if there are no stationary points.
        
    Parameters
    ----------
    fs   : float, optional
        sampling frequency of the data. If not specified this is assumed to be 1
    side : str, optional
        the side of the data to taper, must be one of ``'left'``,
        ``'right'``, or ``'leftright'``
    duration : float, optional
        the duration of time to taper, will override ``nsamples`` if both are provided as arguments
    nsamples : int, optional
        the number of samples to taper, will be overridden by ``duration`` if both are provided as arguments
    window : string, float, or tuple
        The type of window to create. Accepts everything that can be passed to `scipy.signal.get_window <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.get_window.html>`_
       
    Returns
    -------
    out : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        a copy of data tapered at one or both ends
    Raises
    ------
    ValueError
        if ``side`` is not one of ``('left', 'right', 'leftright')``
    """
    # check window properties
    if side not in ('left', 'right', 'leftright'):
        raise ValueError("side must be one of 'left', 'right', or 'leftright'")
        
    if duration:
        nsamples = int(duration * fs)
        
    out = data.copy()
    # if a duration or number of samples is not specified, automatically
    # identify the second stationary point away from each boundary,
    # else default to half the data width
    nleft, nright = 0, 0
    if not nsamples:
        mini, = argrelmin(out)
        maxi, = argrelmax(out)
        
    if 'left' in side:
        nleft = nsamples or max(mini[0], maxi[0])
        nleft = min(nleft, int(data.size/2))
    if 'right' in side:
        nright = nsamples or out.size - min(mini[-1], maxi[-1])
        nright = min(nright, int(data.size/2))
    
    # Define the window
    win_len = (nleft or 0)+(nright or 0)  
    
    win_func = get_window(window=window, Nx=win_len)
    #val("scipy.signal.windows.{}({}, {})".format(window, win_len, win_par))
    
    out[:(nleft or 0)] *= win_func[:(nleft or 0)]
    out[-(nright or 0):] *= win_func[-(nright or 0):]

    return out


def avg_spectro(x, stride, fftlength=None, overlap=None, t0=None, fs=None, window='blackman', average='mean', **psdkwgs):
    """
    Function to compute the averaged spectrogram of a time series ``x``. This is based on `scipy.signal.spectrogram <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html>`_ function, with the key parameters redefined in units of seconds instead of points. This function computes consecutive Fourier transforms of the data. The result is then averaged (approximately) every ``stride`` seconds, according to the selected ``average`` method (classical choices are ``'mean'`` and ``'median'``). Notice that, depending on the choice of ``fftlength``, ``overlap``, and the origninal sampling frequency of the data ``fs``, the output has only approximatively a spacing of ``stride`` seconds.  This is done to avoid data loss, when the number of points in each non-overlapping FFT is not a sub-multiple of the point included in every stride. If you prefer to have exactly ``stride`` seconds spaced estimates, with consequent data loss, make use of the other ``multi_spectro`` method.
    
    Parameters
    ----------
    x : array_like
        Time series of measurement values
    stride : float
        (approximate) number of seconds in single column of spectrogram
    fftlength : float, optional
        length in seconds of the FFT to use to estimate the PSD. Default to the value of ``stride`` if not provided
    overlap :   float, optional
        overlap in seconds of the segments to use for computing the PSD. Defoult is zero
    fs : int, optional 
        sampling frequency of the dataset. Default to 1 if not provided
    window : str, float, or tuple
        The type of window to create. Accepts everything that can be passed to `scipy.signal.get_window <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.get_window.html>`_
    average : str, optional
        Typical choices are ``'mean'`` or ``'median'``. In principle, every other `Average and Variance statistical function of Numpy <https://numpy.org/doc/stable/reference/routines.statistics.html>`_ that can take an array as a single parameter is fine as well (but it is not guaranteed that it'll necessarily make sense, though). E.g.: ``'min'`` and ``'max'`` are legitimate choices (but it is up to you give them a meaningful interpretation)
    **psdkwgs : optional
        other parameters to be passed to `scipy.signal.spectrogram <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html>`_
    
    Returns
    -------
    t : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Array of segment times
    f : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Array of sample frequencies
    Sxx : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Spectrogram of x. By default, the last axis of Sxx corresponds to the segment times
    
    See Also
    --------
    gwdama.preprocessing.preprocessing.multi_spectro
    """
    if not fs:
        fs = 1
    
    # fftlength
    if fftlength is None: 
        nperseg = int(stride*fs) 
    else:
        nperseg = int(fftlength*fs)
    
    # noverlap
    if overlap is None:
        noverlap = 0
    else:
        noverlap = int(overlap*fs)
    
    # nfft, if not specified, is set equal to the next power of two of nperseg (zero padding)
    nfft=psdkwgs.get('nfft', 2**(nperseg - 1).bit_length())
    psdkwgs.update(dict(window=window,
                        nperseg=nperseg,
                        nfft=nfft,
                        fs=fs))   
       
    ff, tt, Sxx = spectrogram(x, **psdkwgs)
    if t0:
        tt +=t0
        
    nstride = sum(tt-tt[0]<stride)
    nmax = (len(tt)//nstride *nstride)
    strides = len(tt)//nstride
    B = Sxx[:,:nmax].reshape(Sxx.shape[0], strides,-1)
    C = eval(f"np.{average}(B,-1)")
    return tt[:nmax:nstride], ff, C


def multi_spectro(x, stride, fftlength=None, overlap=None, t0=None, fs=None, window='blackman', average='mean', nproc=1, **psdkwgs):
    """
    Function to compute a specttrogram  of a time series ``x`` over ultiple processes.
    This is based on `scipy.signal.welch <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html>`_ function, with the key parameters redefined in units of seconds instead of points. This function estimates over different processes the PSD of the data every ``stride`` seconds by means of some modified versions of the Welch's method, that is averaging windowed (and possibly zero padded) FFTs of the data over overlapping segments. Valid averaging methods are the usual ``'mean'`` and ``'median'``, more robust to outliers in the data (such as glitches and other non-stastioarities).
    Notice that, depending on the choice of ``fftlength``, ``overlap``, and the origninal sampling frequency of the data ``fs``, the PSD may not consider the last data in each segment. This happens typically happens when ``fftlength-overlap`` is not a submultiple of the ``stride``. 
    If you prefer to avoid losing data in each segments, but speed speed and time spacing at exactly the value of ``stride`` is not required, the use of the other ``avg_spectro`` function is preferrable. This one is usually faster, though, making use of multiple processes.
    
    Parameters
    ----------
    x : array_like
        Time series of measurement values
    stride : float
        exact number of seconds for each PSD estimate, and therefore in each single column of the spectrogram
    fftlength : float, optional
        length in seconds of the FFT to use to estimate the PSD. Default to the value of ``stride`` if not provided
    overlap :   float, optional
        overlap in seconds of the segments to use for computing the PSD. Defoult is zero
    fs : int, optional 
        sampling frequency of the dataset. Default to 1 if not provided
    window : str, float, or tuple
        The type of window to apply to the FFTs. Accepts everything that can be passed to `scipy.signal.get_window <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.get_window.html>`_. A popular and balanced choice is ``'blackman'``. Other possibilities include ``'hann'``, or ``('tukey', 0.25)``
    average : str, optional
        Available choices are ``'mean'`` or ``'median'``
    nproc : int, optional
        number of CPUs to use in parallel processing of PSDs
    **psdkwgs : optional
        other parameters to be passed to `scipy.signal.welch <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html>`_
    
    Returns
    -------
    t : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Array of segment times
    f : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Array of sample frequencies
    Sxx : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        Spectrogram of x. By default, the last axis of Sxx corresponds to the segment times
        
    See Also
    --------
    gwdama.preprocessing.preprocessing.avg_spectro
    """
    if not fs:
        fs = 1
    nstride = int(stride*fs)
    x_ = x[:(len(x)//nstride *nstride)].reshape(-1,nstride)
    
    time = np.arange(len(x)//nstride)*stride
    if t0:
        time = time + t0
    
    # fftlength
    if fftlength is None: 
        nperseg = nstride 
    else:
        nperseg = int(fftlength*fs)
    
    # noverlap
    if overlap is None:
        noverlap = 0
    else:
        noverlap = int(overlap*fs)
    
    nfft=psdkwgs.get('nfft', 2**(nperseg - 1).bit_length())
    psdkwgs.update(dict(window=window,
                        nperseg=nperseg,
                        nfft=nfft,
                       average=average,
                       fs=fs))   
    
    multipsd = partial(welch, **psdkwgs)
    
    with Pool(processes=nproc) as pool:
        results = np.array(pool.map(multipsd, tuple(x_)))
            
    return time, results[0,0,:], results[:,1,:].T

#####################

def decimate_recursive(data, q_factor, fs = None, **dcmkwgs):
    """
    Downsample the signal in a recursive way after applying an anti-aliasing filter. Notice that when using IIR downsampling, it is recommended to call decimate multiple times for downsampling factors higher than 13. This Decimation cannot be performed for q_factors larger than 13,                
    then it recursively performs decimation with factors lower than                    
    13 searching for multiples of 2, 3 or 5.                                                                                                                                      
    Parameters
    ----------                                                                             
    data : array_like
        The input data
    q_factor : int
        Decimation factor                                

    Returns
    -------
    decim_data : `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ 
        decimated data                                                      
    outfs : int
        New sampling frequency
        
    See Also
    --------
    `scipy.signal.decimate <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.decimate.html#scipy.signal.decimate>`_
        This funtion is a recursive verison of the one implemented in scipy
    """
    if fs is None:
        fs = 1
        
    if q_factor == 1:                                                                      
        #print("q_factor = 1, no need to decimate further...")
        return  data, fs                                                               
    if  q_factor <= 10:                                                                      
        # if decimation factor is larger than 10 it is necessary to decimate many times 
        tg = decimate(data, q_factor, **dcmkwgs)                                                   
        #print(" downsampling by: " + str(q_factor))
        return tg, fs/q_factor                                                     
    else:                                                                              
        if (q_factor%5) == 0:                                                         
            #print(" downsampling by: 5")
            tg = decimate(data,5, **dcmkwgs)                                             
            return decimate_recursive(tg,q_factor/5, fs/5, **dcmkwgs)                      
        elif (q_factor%3) == 0:                                                       
            #print(" downsampling by: 3")                                        
            tg = decimate(data,3,**dcmkwgs)
            return decimate_recursive(tg,q_factor/3, fs/3,**dcmkwgs)
        else : 
            if (q_factor%2) != 0:      
                print(" be carefull, the sampling ratio cannot be divided by 2!!") 
            #tg = scipy.signal.decimate(data,2)  
            tg = decimate(data,2,**dcmkwgs)                                              
            return decimate_recursive(tg,q_factor/2, fs/2,**dcmkwgs)                           

# def psd

#         # number of sample for the fast fourier transform:
#         NFFT = 4 * fs
#         NOVL = -1 * NFFT / 2
#         psd_window = scipy.signal.tukey(NFFT, alpha=1./4)

#         Pxx_H1, freqs = mlab.psd(strain_H1[indxt_around], Fs=fs, NFFT=NFFT,
#                                  window=psd_window, noverlap=NOVL)
#         Pxx_L1, freqs= mlab.psd(strain_L1[indxt_around], Fs=fs, NFFT=NFFT, 
#                                 window=psd_window, noverlap=NOVL)

#         if (plot_others):
#             # smaller window if we're not doing Welch's method
#             short_indxt_away = np.where((time >= time_center - 2) & (
#                 time < time_center + 2))
#             # psd using a tukey window but no welch averaging
#             tukey_Pxx_H1, tukey_freqs = mlab.psd(
#                 strain_H1[short_indxt_away], Fs=fs, NFFT=NFFT, window=psd_window)
#             # psd with no window, no averaging
#             nowin_Pxx_H1, nowin_freqs = mlab.psd(
#                 strain_H1[short_indxt_away], Fs=fs, NFFT=NFFT, 
#                 window=mlab.window_none)

#         # We will use interpolations of the PSDs computed above for whitening:
#         psd_H1 = interp1d(freqs, Pxx_H1)
#         psd_L1 = interp1d(freqs, Pxx_L1)

#
#
#	Npt = int(infs/outfs)           # Number of samples per each segment: infs/outfs= infs*Tout
# 	Nsamples = int(len(signl)/float(Npt)) # Number of segments which the total data frame is divided into
# 	Npseg =  int(Npt/navrg)          # Number of points to include in each fft per segment
# 	Nfft = next_power_of_2(Npseg)

# 	if verbose: print("Npt: {}\nNsamples: {}\nNfft: {}".format(Npt,Nsamples,Nfft))

# 	idx = np.arange(0,Nsamples)*Npt
# 	t = np.arange(0,Nsamples)/outfs

# 	if not isinstance(bands[0],list): bands = [bands]

# 	Nbands = len(bands)

# 	# Initialize BLRMS matrix: (time vector) * (n. bands)
# 	b = np.zeros((len(t), Nbands))

	
# 	if verbose: print('PSD computation for each segment...\n frequency resolution: ',outfs*navrg,'Hz')
# 	# loop over each segment of data

# 	if nproc < 2:
# 	    for i,j in enumerate(idx):
# 	        # compute PSD
# 	        # Same as above
# 	        fr, sx = signal.welch(signl[j:j+Npt], window ='blackman', fs=infs,
# 					noverlap = Npseg/2,  nfft=Nfft, nperseg=Npseg)#, average = 'mean')