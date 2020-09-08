from tkinter import *
from tkinter import filedialog # this module use to open file diolog box
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()#first command to create application

root.title("MP3 Player")#given a title of application	
root.geometry("500x400")# given default geometry
root.iconbitmap(r'music_icon2.ico')

#initialize Pygame
pygame.mixer.init()

#create function to deal with time
def play_time():
	#check to see if song is stopped
	if stopped:
		return 
	#grab current song time
	current_time= pygame.mixer.music.get_pos()/1000
	#grab song time to time format
	converted_current_time= time.strftime('%M:%S', time.gmtime(current_time))

	song=playlist_box.get(ACTIVE)
	song=f'C:/Users/Krishna/MP3 Music Player/audio/{song}.mp3'
	#find current song length
	song_mut= MP3(song)
	global song_length
	song_length=song_mut.info.length

	#convert to time formate
	converted_song_length=time.strftime('%M:%S', time.gmtime(song_length))
	if int(song_slider.get())==int(song_length):
		stop()

	elif paused:
		pass
	else:
		#move slider along 1 second a time
		next_time=int(song_slider.get()) +1
		#output new time value to slider 
		song_slider.config(to=song_length, value=next_time)

		#convert slider position to time format
		converted_current_time= time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

		#output slider
		status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length}')

	#add current time to status bar
	if current_time>0:
		status_bar.config(text=f'Tiem Elapsed: {converted_current_time} of {converted_song_length} ')
	status_bar.after(1000, play_time)



#create finction to add one song
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="chose a song", filetypes=(("mp3 file","*.mp3"),) )# this is cmnd to use open diolog box
	#strip out directory structure and .mp3 from song title
	song=song.replace("C:/Users/Krishna/MP3 Music Player/audio/", "")
	song=song.replace(".mp3", "")
	playlist_box.insert(END, song)

#create function to add many song
def add_many_song():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="chose a song", filetypes=(("mp3 file","*.mp3"),) )# this is cmnd to use open diolog box

	# Loop thrugh song list and replace directory structure for mp3
	for song in songs:
		#strip out directory structure and .mp3 from song title
		song=song.replace("C:/Users/Krishna/MP3 Music Player/audio/", "")
		song=song.replace(".mp3", "")
		# Add to End of playlist
		playlist_box.insert(END, song)

#crete a funciton to delete from a playlist
def delete_song():
	playlist_box.delete(ANCHOR)

#create a function to delete all song from a playlist
def delete_all_song():
	playlist_box.delete(0, END)

#create a play functio
def play():
	#set stopped to false since a song is now playing
	global stopped
	stopped =False

	song=playlist_box.get(ACTIVE)
	song=f'C:/Users/Krishna/MP3 Music Player/audio/{song}.mp3'
	
	# load song with pygame mixer
	pygame.mixer.music.load(song)
	# play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#get song time
	play_time()

#create stopped variable
global stopped
stopped=False

#create a stop function
def stop():
	pygame.mixer.music.stop()
	#clear playlist Bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	#set our slider to zero
	song_slider.config(value=0)
	
	#set stop Variable to True
	global stopped
	stopped=True

#Create Paused Variable
global paused
paused=False

#create a puse function
def pause(is_paused):
	global paused
	paused= is_paused

	if paused:
		#unpaused
		pygame.mixer.music.unpause()
		paused=False
	else:
		#pause
		pygame.mixer.music.pause()
		paused=True

#create function to play the next song
def next_song():
	# reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	#get currrent song number
	next_one=playlist_box.curselection()
	# add one to the current song number tuple/list
	next_one=next_one[0]+1

	#grab the song title from the playlist
	song=playlist_box.get(next_one)
	song=f'C:/Users/Krishna/MP3 Music Player/audio/{song}.mp3'

	# load song with pygame mixer
	pygame.mixer.music.load(song)
	# play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#clear Active Bar in Playlist
	playlist_box.selection_clear(0, END)

	# Move actie bar t\o next song
	playlist_box.activate(next_one)
	#set active bar to next song
	playlist_box.selection_set(next_one, last=None)

#create a function to previous song
def previous_song():
	# reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	#get currrent song number
	next_one=playlist_box.curselection()
	# add one to the current song number tuple/list
	next_one=next_one[0]-1

	#grab the song title from the playlist
	song=playlist_box.get(next_one)
	song=f'C:/Users/Krishna/MP3 Music Player/audio/{song}.mp3'

	# load song with pygame mixer
	pygame.mixer.music.load(song)
	# play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#clear Active Bar in Playlist
	playlist_box.selection_clear(0, END)

	# Move actie bar to next song
	playlist_box.activate(next_one)
	#set active bar to next song
	playlist_box.selection_set(next_one, last=None)

#create volume function 
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#create slide function for song position
def slide(x):
	song=playlist_box.get(ACTIVE)
	song=f'C:/Users/Krishna/MP3 Music Player/audio/{song}.mp3'
	
	# load song with pygame mixer
	pygame.mixer.music.load(song)
	# play song with pygame mixer
	pygame.mixer.music.play(loops=0, start=song_slider.get())


#ceate main frame
main_frame= Frame(root)
main_frame.pack(pady=10)

#create volume slider frame
volume_frame=LabelFrame(main_frame, text="volume")
volume_frame.grid(row=0, column=1, padx=20)

#create volume slider
volume_slider=ttk.Scale(volume_frame, from_=0, to=1, value=1, orient=VERTICAL, length=125, command=volume)
volume_slider.pack(pady=10)

#create Song Slider
song_slider=ttk.Scale(main_frame, from_=0, to=100, value=0, orient=HORIZONTAL, length=360, command=slide)
song_slider.grid(row=2, column=0, pady=10)

#create Playlist Box
playlist_box=Listbox(main_frame, bg="black", fg="white", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

#Create Button Frame
control_frame=Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#Define Button Images For  Controls
back_btn_img=PhotoImage(file='C:/Users/Krishna/MP3 Music Player/images/back50.png')
forward_btn_img=PhotoImage(file='C:/Users/Krishna/MP3 Music Player/images/forward50.png')
play_btn_img=PhotoImage(file='C:/Users/Krishna/MP3 Music Player/images/play50.png')
pause_btn_img=PhotoImage(file='C:/Users/Krishna/MP3 Music Player/images/pause50.png')
stop_btn_img=PhotoImage(file='C:/Users/Krishna/MP3 Music Player/images/stop50.png')


#create Play/stop buttons
back_button=Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button=Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button=Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button=Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))
stop_button=Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#create Menu
my_menu= Menu(root)
root.config(menu=my_menu)

#create Add song menu Dropdows
add_song_menu=Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#add one song to playlist
add_song_menu.add_command(label="Add one song to Playlist", command=add_song)
#add many song to playlist
add_song_menu.add_command(label="Add many song to Playlist", command=add_many_song)
#create delete song menu dropdowns
remove_song_menu=Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="delete a song from a playlist", command=delete_song)
remove_song_menu.add_command(label="delete a many song from a playlist", command=delete_all_song)

#create a status bar
status_bar=Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)
# temporary Label
my_label=Label(root, text='')
my_label.pack(pady=30)

root.mainloop()