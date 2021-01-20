# Multi-TAR uploader for CSCS/Pollux

This code is built on https://github.com/eth-cscs/openstack and has similar [dependencies](https://github.com/eth-cscs/openstack/tree/master/cli)

* pre-configured for CSCS/Pollux authentication
* pre-configured for the Image Service project (```https://object.cscs.ch/v1/AUTH_08c08f9f119744cbbf77e216988da3eb/```)
* expects an already existing container provided as command-line parameter
* user name and password are entered after start
* code grabs all .tar files in the current directory and uploads them as [self-extracting](https://docs.openstack.org/mitaka/user-guide/cli_swift_archive_auto_extract.html)
* a logfile is created with unique name (timestamp-based), recording the container name and progress (time, file, response headers, response content, and a head request following the upload)
* no error handling is provided, but uploaded files are moved into a ```done``` directory (created if does not exist), so code can be simply re-run after Gateway Timeout or similar errors
* code logs in again before starting a new upload if more than 1 hour passed since the previous login

Example usage (assuming ```CSCS_TARs.py``` and the actual ```.tar``` files being in the current directory):

    python CSCS_TARs.py mnm-test-bucket-1
