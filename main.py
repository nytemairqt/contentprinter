from moviepy.editor import * 
import random 
import os 
import tips 

INPUT = 'input/'
OUTPUT = 'output/'
AUDIO = 'audio/'
FONT = 'Bahnschrift'
FONT_COLOR = 'black'
BG_COLOR = 'white'
NUM_VIDEOS = 4

def get_topic(topic):
	if topic == 'guitar production tips':
		topic_dict = tips.guitar_production_tips
	elif topic == 'bass production tips':
		topic_dict = tips.bass_production_tips
	elif topic == 'drum production tips':
		topic_dict = tips.drum_production_tips
	elif topic == 'synth production tips':
		topic_dict = tips.synth_production_tips
	elif topic == 'vocal production tips':
		topic_dict = tips.vocal_production_tips
	elif topic == 'songwriting tips':
		topic_dict = tips.songwriting_tips
	elif topic == 'mixing tips':
		topic_dict = tips.mixing_tips
	elif topic == 'mastering tips':
		topic_dict = tips.mastering_tips
	elif topic == 'random production tips':
		topic_dict = tips.random_tips
	return topic_dict

def create_video(num_clips, filename):	
	clipSeeds = []
	clips = []
	texts = []
	textClips = []
	comps = []

	topic = tips.topics[random.randint(0, len(tips.topics)-1)]
	print(f'Topic: {topic}')
	topic_dict = get_topic(topic)

	# Title Clip & Text
	seed = random.randint(0, len(input_videos)-1)
	prev = seed 	

	# Append first "title" clip
	titleClip = VideoFileClip(f'{INPUT}{input_videos[seed]}')
	titleText = TextClip(f'{(num_clips-1)} {topic}...', font=FONT, fontsize=70, color=FONT_COLOR, bg_color=BG_COLOR).set_duration(5).set_pos('center')
	clips.append(titleClip)	
	textClips.append(titleText)

	# Get Texts
	while len(texts) < num_clips:
		textSeed = random.randint(0, len(topic_dict)-1)
		text = topic_dict[textSeed]	
		if text not in texts:
			texts.append(text)
			textClip = TextClip(f'{text}', font=FONT, fontsize=50, color=FONT_COLOR, bg_color=BG_COLOR, method='caption', size=(600, None)).set_duration(5).set_pos('center')
			textClips.append(textClip)
	
	# Get Clips
	while len(clipSeeds) < num_clips-1:
		seed = random.randint(0, len(input_videos)-1)
		if seed not in clipSeeds:
			clipSeeds.append(seed)
			clip = VideoFileClip(f'{INPUT}{input_videos[seed]}')
			clips.append(clip)	

	# Get Audio
	seed = random.randint(0, len(audio_files)-1)
	print(f'Using audio: {audio_files[seed]}')
	audio_clip = AudioFileClip(f'{AUDIO}{audio_files[seed]}')

	# Composite 
	for i in range(len(clips)):
		comp = CompositeVideoClip([clips[i], textClips[i]])
		comps.append(comp)

	conc = concatenate_videoclips(comps)
	audio_clip.duration = conc.duration
	conc = conc.set_audio(audio_clip) # Doesn't write in place for some reason
	conc.write_videofile(f'{OUTPUT}{filename}')


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

	# Main Loop
	for i in range(NUM_VIDEOS):
		num_clips = random.randint(5, 8)
		print(f'Using {(num_clips-1)} clips.')

		create_video(num_clips, filename=f'{i+1}.mp4')