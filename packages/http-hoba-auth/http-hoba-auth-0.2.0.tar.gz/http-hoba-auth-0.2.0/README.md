# PYTHON HTTP ORIGIN-BOUND AUTHENTICATION SCHEME

Provides utilities for handling HOBA authentication header exchange. See RFC7486 for details.

**NOTE**: At the time of writing this module, the only two signature algorithm codes defined by IANA are RSA-SHA256 and RSA-SHA1 (see RFC section9.3). However, this module was initially written as part of a HOBA implementation for the ethereum/bitcoin secp256k1 signature algorithm. The value "42" is arbitrarily selected for this algorithm, but it by no means pretends to be authoritative.

## Usage

The module is _very_ simple. Refer to the test to see how it works. You'll want to read the RFC too.
