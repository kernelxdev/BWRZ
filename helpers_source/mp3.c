#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: mp3 <YouTube URL>\n");
        return 1;
    }

    char command[512];
    snprintf(command, sizeof(command),
             "yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 \"%s\"",
             argv[1]);

    int result = system(command);

    if (result != 0) {
        fprintf(stderr, "Failed to download MP3. Ensure yt-dlp and FFmpeg are installed.\n");
        return 1;
    }

    printf("MP3 downloaded successfully!\n");
    return 0;
}