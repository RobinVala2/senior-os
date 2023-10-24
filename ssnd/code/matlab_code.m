clc;
clear;
close all;

x = 'SMAIL_CZ_INBOX_1.mp3';
filename = '../audio/orig/';
filename = append(filename, x);


[audio,fvz]=audioread(filename);
filtered_audio = filter(filter_bp, audio);


filename_end = '_AUD.mp3';
path_senior = '../audio/senior/';
filtered_audio_filename = filename(15:end-4);
filtered_audio_filename =append(path_senior, filtered_audio_filename);
filtered_audio_filename = append(filtered_audio_filename, filename_end);


audiowrite(filtered_audio_filename, filtered_audio, fvz);
soundsc(filtered_audio, fvz);
