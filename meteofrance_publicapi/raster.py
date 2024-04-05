"""Functionnalities to deal with the raster data"""
import rasterio
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy import feature


def open_tiff_file(filename):
    with rasterio.open(filename) as src:
        field = src.read(1, masked=True)
        transform = src.transform
    return field, transform

def plot_tiff_file(filename, data_type="temperature"):
    """Open a tiff file an plot it.

    .. note::
        This Function is more an "How-To" rather than a tool to use as is.

    """
    data_field, transform = open_tiff_file(filename=filename)
    # Display the source image with cartopy using the geotransform from the source dataset
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    im = ax.imshow(data_field,
                   cmap='jet',
                   extent=[transform[2],
                           transform[2] + transform[0]*data_field.shape[1],
                           transform[5] + transform[4]*data_field.shape[0],
                           transform[5]])
    ax.add_feature(feature.BORDERS.with_scale('10m'), color='black', linewidth=1)
    ax.add_feature(feature.COASTLINE.with_scale('10m'), color='black', linewidth=1)
    cbar = plt.colorbar(im, ax=ax, shrink=0.5)
    height = filename.stem.split("_")[0]
    computed_at = filename.parent.stem.split("_")[-1]
    if data_type == "temperature":
        cbar.set_label("Temperature (°C)")
        ax.set_title(f"Temperature at {height} above ground \n computed at {computed_at} ")
    add_city_location = False
    if add_city_location:
        lyon_coord = [4.8357, 45.7640]
        paris_coord = [2.3522, 48.8566]
        ax.plot(lyon_coord[0], lyon_coord[1], 'bo', transform=ccrs.PlateCarree())
        ax.plot(paris_coord[0], paris_coord[1], 'bo', transform=ccrs.PlateCarree())
    return ax
