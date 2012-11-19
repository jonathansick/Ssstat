# Ssstat

Amazon S3 Log Processing with MongoDB. **Note that this is entirely experimental. It is not tested for scale, nor does it have a great interface (yet).**

*Ssstat* helps you:

1. Download S3 log files (removing the log glut from your log bucket and archiving them on your hard drive).
2. Parse those log files and add them a MongoDB collection.

Once your log data is in MongoDB it becomes much easier to understand who is accessing your data, and how often.

For a primer on how to get started with S3 logging, refer to the [Setting up Logging](https://github.com/jonathansick/Ssstat/wiki/Setting-up-Logging) page on the project wiki.

## Usage

The UI is terrible.
Using *Cliff* may make the interface more flexible in the future.
Meanwhile, the basic command patterns are:

### To download and ingest event data

  python ssstat.py -b log_bucket_name -p prefix -d cache_dir

This will access your S3 log bucket (`bucket_name`), and download all files with prefix (`prefix`) onto your local HD into the `cache_dir`. After the download is complete, the log files are parsed and ingested into the MongoDB collection for that prefix. Processed log files are deleted from the S3 logging bucket, and moved to the `cache_dir/_prefix_archive` directory. Your log data is never deleted.

### To only ingest log data that has already been downloaded

Suppose you trash the event collection in MongoDB and want to load data back into it. You can re-ingest data from the archive. Simply omit the `-b` argument and *Ssstat* will ingest files already downloaded for that prefix.

  python ssstat.py -p prefix -d cache_dir

## MongoDB Schema

S3 logs are oriented around *prefixes*, where we assume that a unique logging prefix is assigned to each S3 bucket. Prefixes are used to sort logs, and are also used as the names for MongoDB collections.

*Ssstat* stores all its data in a MongoDB database named `ssstat`.
Within that DB, collections are made for each prefix to store event documents.

### Events Documents

Each S3 event is stored in an event document in the prefix's collection.
Fields in this document correspond to S3 log fields, and are:

- `path`: Name of the object (*i.e.,* file) in the bucket being acted on
- `time`: event time, encoded as a `datetime` (UTC) object.
- `ip`: IP address of the requester
- `user_agent`
- `referer`
- `http_status`
- `s3_error`
- `operation`: an operation of `WEBSITE.GET.OBJECT` corresponds to an HTTP access.
- `bytes_sent`

### Event Aggregation

Aggregation statistics are not yet built into *Ssstat*, but see the [Storing Log Data](http://docs.mongodb.org/manual/use-cases/storing-log-data/#counting-requests-by-day-and-page) chapter from the MongoDB manual for a daily download statistic aggregation command.

## Credits

This project relies in [boto][] and [pymongo][] to access AWS S3 and MongoDB, respectively.

Code for S3 log file parsing is based on blog posts by Krzysztof Kowalczyk: [Parsing S3 log files in python](http://blog.kowalczyk.info/article/Parsing-s3-log-files-in-python.html) and [Compacting S3 AWS logs](http://blog.kowalczyk.info/article/Compacting-s3-aws-logs.html).

[boto]: http://docs.pythonboto.org/
[pymongo]: http://api.mongodb.org/python/current/

## Contact info

Tweet me: @jonathansick

## License

Copyright (c) 2012, Jonathan Sick
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
