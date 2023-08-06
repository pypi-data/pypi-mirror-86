Changelog
===========

2.4.0
------
* Stop using matplotlib LaTex fonts in logo plots.

* Pin `biopython` to <1.78 until `Bio.Alphabet` issues fixed in `pyvolve`. See `here <https://github.com/sjspielman/pyvolve/issues/19>`_

2.3.9
------
* Started testing Pep8 compliance with `flake8`

* Removed deprecated `scipy` functions

2.3.8
------
* Fixed bug in `phydms_prepalignment` due to `mafft` shortening sequence names.

2.3.7
------
* Fixed ``scipy`` 2.0.0 deprecation warnings by using ``numpy`` functions in many places rather than ``scipy`` functions. See `here <https://docs.scipy.org/doc/scipy/reference/release.1.4.0.html#deprecated-features>`_.

2.3.6
------
* Revert changes in 2.3.5, they led to numerical errors. Users will have to re-scale preferences when optimizations hits upper bound on parameter.

2.3.5
------
* Increased maximum bound for stringency parameter as the max bound was too low and being hit during optimization in some cases.

2.3.4
------
* Start testing with Python 3.6 and 3.7.

* Remove use of deprecated `Bio.Alphabet`

* Stop using deprecated `natsort.natsorted`

2.3.3
-------
* Fixed `pandas` deprecation bug.

2.3.2
-------
* Option for single color in logo plots.

2.3.1
-----------
* Fix natural sorting of negative numbers in `phydms_logoplot`

* Suppress `matplotlib` backend warnings.

2.3.0
------
* Automate Travis tests

* Only support Python 3.4+

* Swapped basic and acidic colors of ``functionalgroup`` in `weblogo.py`

2.2.2
-----
* Fixed bug in ``spielmanwr``

2.2.1
-----
* Fixed typo in `phydms_comprehensive` output file

* Fixed normalization bug in `Phi_x` calculation, might slightly change numerical values for YNGKP models. This bug fix will generally slightly increase the log likelihoods for YNGKP models.

2.2.0
-----
* Changed computation of ``--omegabysite`` *Q*-values to compute them separately for omega > and < 1. This fixes the issue of many sites of negative selection leading to overly sensitive identification of positive selection.

* Added `utils.modelComparisonDataFrame` function

2.1.4
-------
* Added ``spielmanwr`` calculation to ``ExpCM`` model

* Fixed minor bug with overlays in `weblogo.LogoPlot`

2.1.3
-------
* Added `scalebar` option to `weblogo.LogoPlot`.

2.1.2
-----------
* Fixed ``--colormap`` option to ``phydms_logoplot``.

* Added `underlay` and wildtype overlay bar options to `weblogo.LogoPlot`.

2.1.1
---------
* Altered ``setup.py`` to enable installation without ``numpy`` being pre-installed.

2.1.0
---------
* Added ``--gammabeta`` option to ``phydms``

* Added ``ExpCM`` with ``divpressure`` to ``simulate.py``.

* Updated citation

* Fixed bug in ``simulate.py`` that caused incorrect branch length scalings

* Change installation recommendations

* Fixed installation of ``cython`` extensions.

2.0.5
---------
* Added ``--opt_details`` argument to ``phydms``

* Tweak to likelihood optimization convergence tests

2.0.4
---------
* Minor tweaks to `phydmslib.simulate`

* Fixed rare bug in likelihood optimization that caused nothing to be optimized

2.0.3
---------
* Changes to reduce problems with convergence in ``--diffprefsbysite``

2.0.2
---------
* Added new simulation capabilities to `phydmslib.simulate`

* Added ``--initparams`` option to ``phydms``

* Modified ``--omegabysite`` fitting to reduce (hopefully eliminate) rare errors

2.0.1
---------
* Handle stop codons in preferences

* Change default color scheme for logoplots

* Some minor tweaks to reduce underflow

* Some minor doc updates

2.0.0
-------------
* Compatible with either Python 2.7 or Python 3.4 or greater.

* Completely re-write of the implementation the likelihood calculations. We eliminate the dependence on ``Bio++`` and instead use custom coded calculations without derivatives.

* All tree topology inference is eliminated, some options are removed, numerical values are expected to be slightly different, and speed should be greatly enhanced.

1.3.dev0
-----------
* Added ``--divpressure`` option for analyzing diversifying pressure at sites.

* Added ``--fixationmodel`` option to allow different ways to relate preferences to fixation probabilities.

* In ``phydms_prepalignment``: bug fixes, have ``mafft`` use all available threads, and keep seqs in ``--keepseqs`` regardless of identity to refseq.

* Added ``phydms_testdivpressure``

1.2.5
----------
* Bug fix in ``phydms_prepalignment``

* Added more recent version of ``Bio++`` code

1.2.4
-------
* Added ``phydms_prepalignment`` program.

1.2.3
----------
* Updated docs

* Handle negative MRCAs for ``--dateseqs`` without error

* Added option ``--colormap`` to ``phydms_plotselection``.

* Removed requirements that input sequences be unique in ``alignment``.

1.2.2
--------
* Fixed bug in handling *YNGKP_M7* model in output of ``phydms_comprehensive``

* Added option ``--ncats`` option to set the number of categories for the distributed *omega* in the *YNGKP_M7* and *YNGKP_M8* models.

* Fixed bug in ``--ngammarates`` that caused only one rate to be used.

1.2.1
----------
* Eliminate negative branch lengths to avoid bug in ``biopython`` (<= version 1.66) at parsing them.

1.2.0
------------
* Updated ``Bio++`` again.

* Added ``--dateseqs`` option ``phydms`` and ``phydms_comprehensive``.

* Fixed bug that was making *YNGKP* models always use ``--fitF3X4`` option.

* Added *YNGKP_M1* and *YNKGP_M2* models.

* Changed meaning of ``--yngkp`` option to ``phydms_comprehensive`` to allow multiple or no models beyond *YNGKP_M0*.

* Added ``--gammarates`` option to ``phydms`` and ``phydms_comprehensive``.

* Added env test to ``./tests/``

* Changed source code and docs url from *jbloom* to *jbloomlab* account on ``GitHub``.

1.1.0
-----------
* Updated to newest versions of ``Bio++``

* Added ``--yngkp`` option to ``phydms_comprehensive``, and changed default from *YNGKP_M3* to *YNGKP_M8*.

* Added ``--useLog`` as option to ``phydms`` and ``phydms_comprehensive``, and made differential preferences automatically try logarithms when it encounters problems.

* Added ``--avgrandcontrol`` option to ``phydms_comprehensive``.

* Disallowed identical sequences in ``alignment``.

* Updated to newer versions of ``Bio++``

* Added output for site likelihoods to log file under the fixed stringency parameter when using ``--stringencybysite``.

* Fixed ``--no_optimize`` method for *YNGKP_M3*, *YGNKP_M7*, and *YNGKP_M8* by making program use the old likelihood method for these models.


1.0.2
--------
* Fixed bug in file checks for ``--no_optimize`` option to ``phydms``

* Add ``--no_avgprefs`` option for ``phydms_comprehensive``

1.0.1
--------
* Included ``__*`` files in ``Bpp`` in MANIFEST for proper ``PyPI`` / ``pip`` installation

1.0.0
--------
Initial release
