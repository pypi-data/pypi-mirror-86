#ifndef DROPBEAR_FUZZ_H
#define DROPBEAR_FUZZ_H

#include "config.h"

#if DROPBEAR_FUZZ

#include "includes.h"
#include "buffer.h"
#include "algo.h"
#include "netio.h"
#include "fuzz-wrapfd.h"

// once per process
void fuzz_common_setup(void);
void fuzz_svr_setup(void);
void fuzz_cli_setup(void);

// constructor attribute so it runs before main(), including
// in non-fuzzing mode.
void fuzz_early_setup(void) __attribute__((constructor));

// must be called once per fuzz iteration. 
// returns DROPBEAR_SUCCESS or DROPBEAR_FAILURE
int fuzz_set_input(const uint8_t *Data, size_t Size);

int fuzz_run_server(const uint8_t *Data, size_t Size, int skip_kexmaths, int authdone);
int fuzz_run_client(const uint8_t *Data, size_t Size, int skip_kexmaths);
const void* fuzz_get_algo(const algo_type *algos, const char* name);

// fuzzer functions that intrude into general code
void fuzz_kex_fakealgos(void);
int fuzz_checkpubkey_line(buffer* line, int line_num, char* filename,
        const char* algo, unsigned int algolen,
        const unsigned char* keyblob, unsigned int keybloblen);
extern const char * const * fuzz_signkey_names;
void fuzz_seed(const unsigned char* dat, unsigned int len);

typedef void(*connect_callback)(int result, int sock, void* data, const char* errstring);
struct dropbear_progress_connection *fuzz_connect_remote(const char* remotehost, const char* remoteport,
    connect_callback cb, void* cb_data,
    const char* bind_address, const char* bind_port);

// helpers
void fuzz_get_socket_address(int fd, char **local_host, char **local_port,
                        char **remote_host, char **remote_port, int host_lookup);
void fuzz_fake_send_kexdh_reply(void);
int fuzz_spawn_command(int *ret_writefd, int *ret_readfd, int *ret_errfd, pid_t *ret_pid);
void fuzz_dump(const unsigned char* data, size_t len);

// fake IO wrappers
#ifndef FUZZ_SKIP_WRAP
#define select(nfds, readfds, writefds, exceptfds, timeout) \
        wrapfd_select(nfds, readfds, writefds, exceptfds, timeout)
#define write(fd, buf, count) wrapfd_write(fd, buf, count)
#define read(fd, buf, count) wrapfd_read(fd, buf, count)
#define close(fd) wrapfd_close(fd)
#endif // FUZZ_SKIP_WRAP

struct dropbear_fuzz_options {
    int fuzzing;

    // fuzzing input
    buffer *input;
    struct dropbear_cipher recv_cipher;
    struct dropbear_hash recv_mac;
    int wrapfds;

    // whether to skip slow bignum maths
    int skip_kexmaths;

    // dropbear_exit() jumps back
    int do_jmp;
    sigjmp_buf jmp;

    // write out decrypted session data to this FD if it's set
    // flag - this needs to be set manually in cli-main.c etc
    int dumping;
    // the file descriptor
    int recv_dumpfd;

    // avoid filling fuzzing logs, this points to /dev/null
    FILE *fake_stderr;
};

extern struct dropbear_fuzz_options fuzz;

/* guard for when fuzz.h is included by fuzz-common.c */
#ifndef FUZZ_NO_REPLACE_STDERR

/* This is a bodge but seems to work.
 glibc stdio.h has the comment 
 "C89/C99 say they're macros.  Make them happy." */
/* OS X has it as a macro */
#ifdef stderr
#undef stderr
#endif
#define stderr (fuzz.fake_stderr)

#endif /* FUZZ_NO_REPLACE_STDERR */

struct passwd* fuzz_getpwuid(uid_t uid);
struct passwd* fuzz_getpwnam(const char *login);
/* guard for when fuzz.h is included by fuzz-common.c */
#ifndef FUZZ_NO_REPLACE_GETPW
#define getpwnam(x) fuzz_getpwnam(x)
#define getpwuid(x) fuzz_getpwuid(x)
#endif // FUZZ_NO_REPLACE_GETPW

#endif // DROPBEAR_FUZZ

#endif /* DROPBEAR_FUZZ_H */
