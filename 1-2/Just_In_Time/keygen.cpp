#include <iostream>
#include <ctime>
#include <cstring>
#include <cstddef>

using namespace std;

void keygen(char *key, tm *local_time)
{
    // simple stuff
    key[0] = '%';
    key[3] = 'k';
    key[6] = '^';
    key[9] = 'f';
    key[12] = 'F';

    // complicated stuff
    int result = 0;
    for (int i = 0; i < 256; i++) {
        result = i & 0x3fffffff;

        switch (result) {
        case 46:
            key[8] = i;
            break;
        case 49:
            key[11] = i;
            break;
        case 57:
            key[5] = i;
            break;
        }
    }

    int secs_mod = (local_time->tm_sec % 10) % 3;

    for (int i = 0; i < 128; i++) {
        result = i << secs_mod;

        switch (result) {
        case 80:
            key[4] = i;
            break;
        case 104:
            key[13] = i;
            break;
        case 128:
            key[10] = i;
            break;
        case 200:
            key[1] = i;
            break;
        case 212:
            key[2] = i;
            break;
        case 246:
            key[7] = i;
            break;
        }
    }

    key[15] = '\0';
}

int main()
{
    char key[16] = "00000000000000";

    // get current local time
    time_t global_time{};
    tm *local_time{};

    time(&global_time);
    local_time = localtime(&global_time);

    keygen(key, local_time);

    cout << key << endl;

    return 0;
}
