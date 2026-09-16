def shift_range_back(time_range, shift_time):
    """
    Subtracts shift_time from both the start and end of a time range.
    
    Example:
      time_range = "2:00-5:00"
      shift_time = "1:05"
      Returns: "00:55-3:55"
    """
    start_str, end_str = [t.strip() for t in time_range.split('-')]
    
    start_sec = time_to_sec(start_str)
    end_sec = time_to_sec(end_str)
    shift_sec = time_to_sec(shift_time)
    
    # Subtract from both sides
    new_start_sec = start_sec - shift_sec
    new_end_sec = end_sec - shift_sec
    
    return f"{sec_to_time(new_start_sec)}-{sec_to_time(new_end_sec)}"

def time_to_sec(t_str):
    """Converts '1:05' or '01:05:10' into total seconds (float)."""
    parts = list(map(float, t_str.strip().split(':')))
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]

def sec_to_time(seconds):
    """Converts total seconds back into 'M:SS' format."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

def merge_timestamps(timestamps):
    if not timestamps:
        return []

    # 1. Parse strings into numerical ranges (start_sec, end_sec)
    parsed_ranges = []
    for item in timestamps:
        # Handles single string items or comma-separated strings inside items
        sub_items = item.split(',')
        for sub in sub_items:
            if '-' in sub:
                start_str, end_str = sub.split('-')
                parsed_ranges.append((time_to_sec(start_str), time_to_sec(end_str)))

    # 2. Sort ranges by their start time
    parsed_ranges.sort(key=lambda x: x[0])

    # 3. Merge overlapping or touching ranges
    merged = [parsed_ranges[0]]
    for current_start, current_end in parsed_ranges[1:]:
        prev_start, prev_end = merged[-1]

        # If current interval overlaps or touches the previous interval
        if current_start <= prev_end:
            # Extend end to the highest value (forward extension)
            merged[-1] = (prev_start, max(prev_end, current_end))
        else:
            merged.append((current_start, current_end))

    # 4. Convert seconds back to time string format
    return [f"{sec_to_time(s)}-{sec_to_time(e)}" for s, e in merged]

def get_unblurred_stamps(file_path, merged_blur):
    # 2. Get total video duration in seconds using OpenCV
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_duration = total_frames / fps
    cap.release()
    
    if not merged_blur:
        return [f"0:00-{sec_to_time(video_duration)}"]
    
    unblurred = []
    current_time = 0.0
    
    # 3. Find gaps between blurred ranges
    for stamp in merged_blur:
        start_str, end_str = stamp.split('-')
        blur_start = time_to_sec(start_str)
        blur_end = time_to_sec(end_str)
        
        # If there is a gap before the next blur start, save it
        if blur_start > current_time:
            unblurred.append(f"{sec_to_time(current_time)}-{sec_to_time(blur_start)}")
            
        current_time = max(current_time, blur_end)
    
    # 4. Catch any remaining video length after the last blur range
    if current_time < video_duration:
        unblurred.append(f"{sec_to_time(current_time)}-{sec_to_time(video_duration)}")
        
    return unblurred

def combine_and_sort_stamps(stamps, rest_stamps):
    combined = stamps + rest_stamps
    # Sort chronologically by start time in seconds
    combined.sort(key=lambda stamp: time_to_sec(stamp.split('-')[0]))
    return combined

def Vid_Frag(file_path,fullstamps,isunblur=False): 
    Parts = []
    for stamp in fullstamps : 
      part,cap = Media_Trim(file_path,stamp)
      if isunblur : 
        Parts.append(part)
      else : 
        Parts.append((part,stamp))
    return Parts

def Blur_Ranges(file_path,Rate,Blur_File):
  Keys = [k for k, v in Blur_File.items() if not isinstance(v, bool) and v != ""]
  TimeStamps = [v for k, v in Blur_File.items() if isinstance(v, str) and v != ""]  
  stamps = merge_timestamps(TimeStamps)
  rest_stamps = get_unblurred_stamps(file_path,stamps)
  fullstamps = combine_and_sort_stamps(stamps,rest_stamps)
  blurParts = Vid_Frag(file_path,stamps)
  bluredParts = []
  unblurParts = Vid_Frag(file_path,rest_stamps,True)
  for part in blurParts : 
    blurfile = {'isfull':True,'MainBlur':'','RightHalf':'','LeftHalf':'','UpperHalf':'','LowerHalf':'','RightThird':'','LeftThird':'','UpperThird':'','LowerThird':'','RightThirdLeft':'','LeftThirdLeft':'','UpperThirdLeft':'','LowerThirdLeft':'','FullFrame':'','RightHalfK':False,"LeftHalfK":False,"UpperHalfK":False,"LowerHalfK":False,"RightThirdK":False,"LeftThirdK":False,"UpperThirdK":False,"LowerThirdK":False,"RightThirdLeftK":False,"LeftThirdLeftK":False,"UpperThirdLeftK":False,"LowerThirdLeftK":False,"FullFrameK":False}
    blurfile['isfull'] = False
    start = part[1].split('-')[0]
    for key in Keys :
      time_val = Blur_File[key]
      if isinstance(time_val, tuple):
        time_val = time_val[1]
      if isinstance(time_val, str) and time_val != "":
         blurfile[key] = shift_range_back(time_val, start) 
    Res_Part = Raw_Blur(part[0],Rate,blurfile)
    bluredParts.append(Res_Part)
  stamp_to_file = {**dict(zip(stamps, bluredParts)), **dict(zip(rest_stamps, unblurParts))}
  fullparts = [stamp_to_file[stamp] for stamp in fullstamps]
  Ext = '.' + file_path.split('.')[-1]
  mergtxt = file_path.replace(Ext,'.txt')              
  for File_Elm in fullparts :
    Main_Dir = ('.' if File_Elm[0] == '.' else '' ) + ('/'.join(File_Elm.split('/')[:-1])) + '/'
    New_Name = f"Vid_{random.randint(0,1000)}.mp4"
    New_File = Main_Dir+New_Name
    os.rename(File_Elm,New_File)
    open(mergtxt,'a').write(f"file '{New_File}' \n")
  Res_File = Vid_Merge(mergtxt)
  return Res_File

import langid

async def Detect_Lang(Text) : 
  lang, confidence = langid.classify(Text)
  return lang
