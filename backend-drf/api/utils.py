# import os
# from django.conf import settings
# import matplotlib.pyplot as plt


# def save_plot(plot_img_path):
#     image_path = os.path.join(settings.MEDIA_ROOT,plot_img_path)
#     plt.savefig(image_path)
#     plt.close()
#     image_url = os.path.join(settings.MEDIA_ROOT,plot_img_path)
#     return image_url

import os
from django.conf import settings
import matplotlib.pyplot as plt

def save_plot(plot_img_path):
    # Save image to media folder
    image_path = os.path.join(settings.MEDIA_ROOT, plot_img_path)
    plt.savefig(image_path)
    plt.close()

    # Return URL that can be served to frontend
    return f"{settings.MEDIA_URL}{plot_img_path}"
