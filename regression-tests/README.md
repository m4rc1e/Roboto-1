# WIP: Visual diff between original Roboto and Roboto TN

Comparing Google's unhinted Roboto [v2.138](https://github.com/google/roboto/releases/tag/v2.138) against TN's VF Roboto, https://github.com/TypeNetwork/Roboto/tree/fea-fix-mark-mkmk/Roboto-VF.tttf



## How

Instances are generated from the VF font using fontTools.varLib.mutator
Instances are compared against the ttfs in roboto-2.138 dir using [gfdiffbrowsers](https://github.com/googlefonts/diffbrowsers)
## Installation

You will need a [Browserstack account](https://www.browserstack.com)

```
virtualenv venv --python=python2
source venv/bin/activate
pip install gfdiffbrowsers
pip install fonttools
```

To generate diff images run:

`python generate_diffs.py`

Please note the BrowserStack api is very slow