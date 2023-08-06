from PIL import Image, ImageTk
from tkinter import *
from pdf2image import convert_from_path
import click
from os import path

@click.group()
def cli():
    pass


@cli.command()
@click.argument('file', required=True)
def show(file):
    '''
    View a PDF file.
    '''
    filepath = path.abspath(file)

    window = Tk()

    window.title(f"PDF Viewer - {filepath}")

    pdf_frame = Frame(window).pack(fill=BOTH)
    scroll_y = Scrollbar(pdf_frame, orient=VERTICAL)
    pdf = Text(pdf_frame, yscrollcommand=scroll_y.set, bg='grey')

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_y.config(command=pdf.yview)

    pdf.pack(fill=BOTH, expand=1)

    pages = convert_from_path(filepath, size=(800, 900))

    photos = []

    for i in range(len(pages)):
        photos.append(ImageTk.PhotoImage(pages[i]))

    for photo in photos:
        pdf.image_create(END, image=photo)

        pdf.insert(END, '\n\n')

    window.mainloop()


if __name__ == "__main__":
    cli()