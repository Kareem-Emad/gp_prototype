class video_indexer:
    def extract_clips(self, flushed_tags):
        clip_start_index = -1
        clips = []

        # padding so we don't start without a 01 transition or end without 10
        flushed_tags = [False] + flushed_tags + [False]

        for idx in range(1, len(flushed_tags)):
            if(flushed_tags[idx - 1] != flushed_tags[idx]):  # is there is a transition
                if(flushed_tags[idx]):  # 0 1 transition => period start
                    clip_start_index = idx
                else:  # 1 0 transistion => period end
                    if(idx - clip_start_index - 1 > 10):
                        clips.append((clip_start_index - 1, idx - 2))

        return clips
