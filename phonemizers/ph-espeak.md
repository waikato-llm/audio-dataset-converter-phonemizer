# ph-espeak

Uses the espeak backend of the phonemizer library: https://github.com/bootphon/phonemizer
For available languages see: https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md

```
usage: ph-espeak [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-N LOGGER_NAME] [--disable] [-L LANGUAGE] [--strip]
                 [--preserve_empty_lines] [--preserve_punctuation]
                 [--njobs NJOBS]

Uses the espeak backend of the phonemizer library:
https://github.com/bootphon/phonemizer For available languages see:
https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md

options:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
  -N LOGGER_NAME, --logger_name LOGGER_NAME
                        The custom name to use for the logger, uses the plugin
                        name by default (default: None)
  --disable             Whether to disable the phonemizer (default: False)
  -L LANGUAGE, --language LANGUAGE
                        The language of the speech data, e.g., 'en-us'.
                        (default: en-us)
  --strip               Whether to omit the last word and phone separators of
                        a token. (default: False)
  --preserve_empty_lines
                        Whether to keep empty lines. (default: False)
  --preserve_punctuation
                        Whether to keep punctuation. (default: False)
  --njobs NJOBS         The number of jobs to execute in parallel. (default:
                        1)
```
