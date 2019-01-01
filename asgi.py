import os
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ohq.settings")
channel_layer = get_channel_layer()