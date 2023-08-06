# Draw and process B-NMR CCD image files

## Installation and Running the GUI

* Install with `pip3 install --user bccd` from [pypi](https://pypi.org/project/bccd/). 
* Run with `python3 -m bccd`. You may want to create an alias for this command. 

Note that `bccd` uses `rsync` to copy all files from the machines which operate the cameras. These machines are password protected and the passwords must be entered on every use, unless you give your public key to these devices. To do that, do:

* Create a public key if you don't have one already: `ssh-keygen -t rsa`. On prompt enter no password. 
* Copy the key to the server using the proper username and password: `ssh-copy-id user@machine.domain`

On first usage, `bccd` will need to transfer all the files from these machines. This may take some time, please be patient. On subsequent usages, `bccd` will only update its list of files so the process will be much faster. These files are stored in `$HOME/.bccd`.

## `bccd.fits` Reference

Constructor: 

```python
fits(filename,rescale_pixels=True)
```

Functions: 
    
```python

# look for shapes in image
detect_lines(sigma=1,min_length=50,min_gap=3,theta=None,nlines=np.inf,draw=True)
detect_hlines(sigma=1,min_length=50,min_gap=3,nlines=np.inf,draw=True,**kwargs)
detect_circles(rad_range,nlines=1,sigma=1,draw=True)

# drawing and visualization
draw(black=0,alpha=1,cmap='Greys',imap=True)
draw_2Dfit(fn,*pars,levels=10,cmap='jet')
draw_contour(nlevels=5,alpha=1,cmap='Greys',imap=True)
draw_edges(sigma=1,alpha=1,cmap='Greys',imap=True) 
draw_sobel(alpha=1,cmap='Greys',imap=False)

# fitting
fit2D(function,**fitargs)
fit_gaussian2D(draw=True,**fitargs)

# processing
get_center(draw=True)
get_cm(draw=True)
get_gaussian2D_overlap(ylo,yhi,xlo,xhi)

# worker functions
read(filename,rescale_pixels=True)
set_black(black)
set_mask(mask)
```

Data fields:

```
black:          float, pixel value corresponding to black (zero)
data:           2D numpy array, pixel values
data_original:  numpy array, pixel values
header:         dict, header information

mask:           (x,y,r) specifying circle to mask on

result_center:      (par,names) fitting results
result_cm:          (par,names) center of mass results
result_fit2D:       (par,cov) fitting results
result_gaussian2D:  (par,cov,names) fitting results
result_gaussian2D_overlap: float, overlap
```

Some useful colourmap names:

```
    Greys
    Purples
    Yellows
    Blues
    Oranges
    Reds
    Greens
```

Parameter descriptions

```
alpha:          float, image transparency. Range: [0,1].
black:          float, value to set to black, all pixels of lower value raised to this level. Use to
                clean up noise. 

cmap:           str, color map to color the image. Ex: "Reds", "Greens", etc.
draw:           bool, if true, draw output
filename:       str, path to .fits file
fitargs:        **dict, arguments passed to curve_fit
fn:             function handle, function to draw
imap:           bool, if True, invert color map colours
levels:         int, number of contour levels to draw
kwargs:         **dict, unused
mask:           tuple, exclude all pixels outside of circle from draw or calculation. (x0,y0,r)
min_length:     float, minimum length of lines to find, in pixels
min_gap:        float, maximum acceptable distance between line pixels which do not signify breaking
                the line
nlines:         int, number of shapes to find
pars:           *tuple, parameters passed to fn. 
rad_range:      tuple, radius range to seach in (r_lo, r_hi)
rescale_pixels: bool, pixels are intrinsically asymmetric. Rescale image such that the pixels are 
                square, interpolating pixel values with 3rd order spline. 
shape:          tuple, shape of the image (number of pixels x,y)
sigma:          float, standard deviation of rolling Gaussian filter, smoothing image features.
theta:          float, list of acceptable angles for the lines to point

xlo:              function handle, lower integration bound [inner]
xlhi:             function handle, upper integration bound [inner]
ylo:              float, lower integration bound [outer]
yhi:              float, upper integration bound [outer]
```



## `bccd.functions`

```python
gaussian2D(x,y,x0,y0,sigmax,sigmay,amp,theta=0)
```

Parameter descriptions

```
amp:              float, unused in favour of normalized amplitude (present for ease of use)
sx,sy:            float, standard deviation
theta:            float, angle of rotation                  
x0,y0:            float, gaussian mean location
```
