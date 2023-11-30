import streamlit as st
import os
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import base64

# Fonction pour ajouter du texte à une image
def add_text_to_image(image, text):
    image_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(image_pil)

    # Utiliser la police Calibri (taille 12, en blanc)
    font_path = "C:/Windows/Fonts/calibri.ttf"  # Chemin vers la police Calibri
    font_size = 11
    font = ImageFont.truetype(font_path, font_size)

    # Ajouter le texte en blanc au coin supérieur gauche
    draw.text((10, 10), text, font=font, fill=(255, 140, 0))  # Remplissage en blanc

    return np.array(image_pil)

# Dossier contenant les images pour chaque propriété
base_folder = "https://assatfatima.github.io/image/raster_streamlit/"
properties = ['reussite', 'difficute', 'engagement']

# Durée d'affichage de chaque image en secondes
duration_per_image = 3 # Vous pouvez ajuster cette valeur pour changer la vitesse de l'animation

# Boucler à travers chaque propriété
for prop in properties:
    # Liste des chemins d'accès aux images pour la propriété actuelle
    images = [os.path.join(base_folder, f'{prop}{i}.tif') for i in range(1,7)]

    # Liste des dates correspondantes aux images pour la propriété actuelle
    dates = [f'{prop}_jour{-i}' for i in range(1,7)]

    # Chemin de sortie pour la vidéo
    output_directory = 'C:\Users\HP\Desktop\STREAMLIT_IMAGES'
    output_path = os.path.join(output_directory, f'timelapse_{prop}.mp4')

    # Créer un éditeur vidéo imageio
    video_writer = imageio.get_writer(output_path, fps=2/duration_per_image)

    # Boucler à travers chaque paire image-date et ajouter à la vidéo
    for image_path, date in zip(images, dates):
        # Charger l'image
        img = imageio.imread(image_path)

        # Ajouter du texte avec la date sur l'image
        img_with_text = add_text_to_image(img, date)

        # Ajouter l'image à la vidéo
        video_writer.append_data(img_with_text)

    # Fermer l'éditeur vidéo
    video_writer.close()

    # Liste des noms des vidéos
videos = ['timelapse_reussite.mp4', 'timelapse_difficute.mp4', 'timelapse_engagement.mp4']
    #['reussite', 'difficute', 'engagement']
    # Liste des noms des GIFs à créer
gifs = ['timelapse_reussite.gif', 'timelapse_difficute.gif', 'timelapse_engagement.gif']

    # Durée d'affichage de chaque image dans le GIF (en secondes)
duree_image_gif = 12  # Augmenter la durée d'affichage par image pour ralentir le GIF

    # Vitesse du GIF
vitesse_gif = 1.5  # Réduire cette valeur pour ralentir davantage le GIF

    # Créer les GIFs à partir des vidéos
for video, gif in zip(videos, gifs):
    chemin_video = os.path.join(output_directory, video)
    chemin_gif = os.path.join(output_directory, gif)

    # Lire la vidéo avec imageio
    reader = imageio.get_reader(chemin_video)
    # Créer le GIF avec imageio
    writer = imageio.get_writer(chemin_gif, duration=duree_image_gif, fps=vitesse_gif)

    # Ajouter chaque image de la vidéo au GIF
    for image in reader:
        writer.append_data(image)

        # Fermer le writer
    writer.close()

# Fonction pour lire le contenu du fichier en base64
def get_gif_base64(file_path):
    with open(file_path, "rb") as file:
        contents = file.read()
        return base64.b64encode(contents).decode("utf-8")

# Sélectionner la propriété ('reussite', 'difficute', 'engagement')
selected_property = st.selectbox('Sélectionner une propriété', ['reussite', 'difficute', 'engagement'])

# Déterminer le chemin du fichier en fonction de la propriété choisie
file_path = f"C:/Users/hp/Desktop/dashbord/video/timelapse_{selected_property}.gif"

# Afficher le GIF en utilisant la fonction avec un style CSS pour la taille
st.markdown(
    f'<img src="data:image/gif;base64,{get_gif_base64(file_path)}" alt="{selected_property} gif" style="width:700%; height:450;">',
    unsafe_allow_html=True,
)

print("Vidéos et GIFs créés avec succès.")
