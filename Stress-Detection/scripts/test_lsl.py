from pylsl import StreamInlet, resolve_byprop
import time

# Resolve EEG stream by property
print("🔍 Looking for EEG stream...")
streams = resolve_byprop('type', 'Data', timeout=10)
if not streams:
    print("❌ No EEG stream found. Make sure UnicornLSL is running.")
    exit()

# Create inlet
inlet = StreamInlet(streams[0])
info = inlet.info()
info = inlet.info()
ch = info.desc().child('channels').child('channel')
labels = []

for i in range(info.channel_count()):
    label = ch.child_value('label') or f"Chan-{i}"
    labels.append(label)
    print(f"{i}: {label}")
    ch = ch.next_sibling()

# Print stream metadata
print("\n🔷 Stream Info:")
print(f"Name: {info.name()}")
print(f"Type: {info.type()}")
print(f"Sampling Rate: {info.nominal_srate()} Hz")
print(f"Channels: {info.channel_count()}")
print(f"Source ID: {info.source_id()}")

# Get channel labels from stream description
print("\n🔷 Channel Labels (in order):")
labels = []
ch = info.desc().child('channels').child('channel')
for i in range(info.channel_count()):
    label = ch.child_value('label')
    labels.append(label)
    print(f"{i}: {label}")
    ch = ch.next_sibling()

# Read and print sample data
print("\n🔷 Streaming samples (press Ctrl+C to stop)...")
try:
    while True:
        sample, timestamp = inlet.pull_sample()
        if sample:
            formatted = ', '.join(f"{labels[i]}: {val:.2f}" for i, val in enumerate(sample))
            print(f"{timestamp:.3f} => {formatted}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n✅ Stream stopped.")
