#! python3
import whisper
import click

def _whisper_result_to_srt(result):
    print("Convert to srt")
    text = []
    for i,s in enumerate(result['segments']):
        text.append(str(i+1))

        time_start = s['start']
        hours, minutes, seconds = int(time_start/3600), (time_start/60) % 60, (time_start) % 60
        timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_start = timestamp_start.replace('.',',')     
        time_end = s['end']
        hours, minutes, seconds = int(time_end/3600), (time_end/60) % 60, (time_end) % 60
        timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_end = timestamp_end.replace('.',',')        
        text.append(timestamp_start + " --> " + timestamp_end)

        text.append(s['text'].strip() + "\n")
            
    return "\n".join(text)

@click.command()
@click.option('--in', 'file_in', help='Takes an audio file.', required=True)
@click.option('--out', help='Output file name.', default='result.srt')
@click.option('--model', help='Model to use.', type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']), default='small')
@click.option('--english', help='Only use the english model (not available for large)', is_flag=True, default=False)
def work(file_in, out, model, english):
    
    if english and not model == "large":
        print("English only model selected.")
        model = "{}.en".format(model)

    print("Loading model: {}".format(model))
    model = whisper.load_model(model)
    print("Transcribing audio...")
    result = model.transcribe(file_in)

    with open(out, "w") as my_file:
        my_file.write(_whisper_result_to_srt(result))
    print("done")


if __name__ == '__main__':
    work()