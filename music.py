from moviepy.editor import * 
import random 
import os 
from tqdm import tqdm

INPUT = 'musicVideos/'
OUTPUT = 'output/'
AUDIO = 'musicAudio/'
FONT = 'Bahnschrift'
FONT_COLOR = 'black'
BG_COLOR = 'white'
FFO = ['Bad Omens', 'BMTH', 'Sleep Token', 'Tool', 'Deftones', 'Spiritbox']

def create_music_video(audio_clip, track_title):
	clipSeeds = []
	clips = []
	comps = []

	track_length = int(audio_clip.duration)
	video_length = 0
	seed = -1
	prev_seed = -1

	# Get Clips
	while video_length < track_length:
		if seed != -1:
			prev_seed = seed # Non-repeating
		seed = random.randint(0, len(input_videos)-1) 
		while seed == prev_seed:
			seed = random.randint(0, len(input_videos)-1) 
		clip = VideoFileClip(f'{INPUT}{input_videos[seed]}')

		# Random reverse X 
		reverse = random.randint(0, 1)
		if reverse:
			clip = clip.fx(vfx.mirror_x)
		clip_length = random.randint(1, 2)

		# Trim if final clip will be too long
		if video_length + clip_length > track_length:
			clip_length = track_length - video_length

		clip.duration = clip_length

		# Append clip and redetermine length
		video_length += clip_length
		clips.append(clip)

	print('appended clips...')
	print(f'track length: {track_length}')
	print(f'final video length: {video_length}')



	text = f"here's my song: '{track_title[:-6]}'"
	band1 = random.randint(0, len(FFO)-1)
	band2 = random.randint(0, len(FFO)-1)
	while band2 == band1:
		band2 = random.randint(0, len(FFO)-1)
	band3 = random.randint(0, len(FFO)-1)
	while band3 == band1 or band3 == band2:
		band3 = random.randint(0, len(FFO)-1) 

	ffo = f'FFO: {FFO[band1]}, {FFO[band2]}, {FFO[band3]}'
	stream = f'full song on my channel'

	# Composite Caption
	text_duration = 4
	text_clip1 = TextClip(f'{text}', font=FONT, fontsize=70, color=FONT_COLOR, bg_color=BG_COLOR, method='caption', size=(600, None)).set_duration(text_duration).set_pos('center')
	text_clip2 = TextClip(f'{ffo}', font=FONT, fontsize=70, color=FONT_COLOR, bg_color=BG_COLOR, method='caption', size=(600, None)).set_duration(text_duration).set_pos('center')
	text_clip3 = TextClip(f'{stream}', font=FONT, fontsize=70, color=FONT_COLOR, bg_color=BG_COLOR, method='caption', size=(600, None)).set_duration(text_duration).set_pos('center')
	final_text = concatenate_videoclips([text_clip1, text_clip2, text_clip3]).set_pos('center')

	conc = concatenate_videoclips(clips)
	conc = CompositeVideoClip([conc, final_text])
	conc = conc.set_audio(audio_clip) # Doesn't write in place for some reason
	conc.write_videofile(f'{OUTPUT}{track_title}')


if __name__ == '__main__':

	# Gather Input Videos
	input_videos = []
	for root, dirs, files in os.walk(INPUT):
		for name in files:
			input_videos.append(name)

	# Gather Audio Files
	audio_files = []
	for root, dirs, files in os.walk(AUDIO):
		for name in files:
			audio_files.append(name)

	NUM_VIDEOS = int(len(audio_files)) # For every music clip

	# Main Loop
	for i in tqdm(range(NUM_VIDEOS)):
		audio_clip = AudioFileClip(f'{AUDIO}{audio_files[i]}')
		track_title = f'{audio_files[i][:-4]}.mp4' # Truncate Previous File Extension

		create_music_video(audio_clip=audio_clip, track_title=track_title)		