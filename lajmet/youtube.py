import logging
import urllib.request
import xml.etree.ElementTree as ET

from django.core.cache import cache

logger = logging.getLogger(__name__)

CHANNEL_ID = "UCgoIqClR2vtRk3L2X_abDTA"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

CACHE_KEY = "yt_videot_e_fundit"
CACHE_SEKONDA = 600          # rifreskohet çdo 10 minuta
CACHE_FALLBACK_SEKONDA = 60  # nëse dështon, provon prapë pas 1 minute

# Videot që shfaqen nëse YouTube nuk përgjigjet
FALLBACK = [
    {"id": "KxZQDFELNVU", "titulli": ""},
    {"id": "Ix0lO1v0Uk4", "titulli": ""},
    {"id": "ufRy7OTX_lE", "titulli": ""},
]

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def _lexo_feed():
    req = urllib.request.Request(
        FEED_URL, headers={"User-Agent": "Mozilla/5.0 (KonfidencialeNews)"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        root = ET.fromstring(resp.read())

    videot = []
    for entry in root.findall("atom:entry", NS):
        vid = entry.findtext("yt:videoId", default="", namespaces=NS)
        titulli = entry.findtext("atom:title", default="", namespaces=NS)
        if vid:
            videot.append({"id": vid, "titulli": titulli})
    return videot


def merr_videot_e_fundit(limit=3):
    videot = cache.get(CACHE_KEY)
    if videot is None:
        try:
            videot = _lexo_feed()
        except Exception as e:
            logger.warning("YouTube feed dështoi: %s", e)
            videot = []

        if videot:
            cache.set(CACHE_KEY, videot, CACHE_SEKONDA)
        else:
            videot = FALLBACK
            cache.set(CACHE_KEY, videot, CACHE_FALLBACK_SEKONDA)

    return videot[:limit]