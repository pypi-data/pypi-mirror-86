
Changelog
=========

3.7.0 (2020-11-20)
------------------

* Made logger names more specific. Now can have granular filtering on these new logger names:

  * ``redis_lock.acquire`` (emits `DEBUG` messages)
  * ``redis_lock.acquire`` (emits `WARN` messages)
  * ``redis_lock.acquire`` (emits `INFO` messages)
  * ``redis_lock.refresh.thread.start`` (emits `DEBUG` messages)
  * ``redis_lock.refresh.thread.exit`` (emits `DEBUG` messages)
  * ``redis_lock.refresh.start`` (emits `DEBUG` messages)
  * ``redis_lock.refresh.shutdown`` (emits `DEBUG` messages)
  * ``redis_lock.refresh.exit`` (emits `DEBUG` messages)
  * ``redis_lock.release`` (emits `DEBUG` messages)

  Contributed by Salomon Smeke Cohen in `#80 <https://github.com/ionelmc/python-redis-lock/pull/80>`_.
* Fixed few CI issues regarding doc checks.
  Contributed by Salomon Smeke Cohen in `#81 <https://github.com/ionelmc/python-redis-lock/pull/81>`_.

3.6.0 (2020-07-23)
------------------

* Improved ``timeout``/``expire`` validation so that:

  - ``timeout`` and ``expire are converted to ``None`` if they are falsy. Previously only ``None`` disabled these options, other falsy
    values created buggy situations.
  - Using ``timeout`` greater than ``expire`` is now allowed, if ``auto_renewal`` is set to ``True``. Previously a ``TimeoutTooLarge`` error
    was raised.
    See `#74 <https://github.com/ionelmc/python-redis-lock/issues/74>`_.
  - Negative ``timeout`` or ``expire`` are disallowed. Previously such values were allowed, and created buggy situations.
    See `#73 <https://github.com/ionelmc/python-redis-lock/issues/73>`_.
* Updated benchmark and examples.
* Removed the custom script caching code. Now the ``register_script`` method from the redis client is used.
  This will fix possible issue with redis clusters in theory, as the redis client has some specific handling for that.

3.5.0 (2020-01-13)
------------------

* Added a ``locked`` method. Contributed by Artem Slobodkin in `#72 <https://github.com/ionelmc/python-redis-lock/pull/72>`_.

3.4.0 (2019-12-06)
------------------

* Fixed regression that can cause deadlocks or slowdowns in certain configurations.
  See: `#71 <https://github.com/ionelmc/python-redis-lock/issues/71>`_.

3.3.1 (2019-01-19)
------------------

* Fixed failures when running python-redis-lock 3.3 alongside 3.2.
  See: `#64 <https://github.com/ionelmc/python-redis-lock/issues/64>`_.

3.3.0 (2019-01-17)
------------------

* Fixed deprecated use of ``warnings`` API. Contributed by Julie MacDonell in
  `#54 <https://github.com/ionelmc/python-redis-lock/pull/54>`_.
* Added ``auto_renewal`` option in ``RedisCache.lock`` (the Django cache backend wrapper). Contributed by c
  in `#55 <https://github.com/ionelmc/python-redis-lock/pull/55>`_.
* Changed log level for "%(script)s not cached" from WARNING to INFO.
* Added support for using ``decode_responses=True``. Lock keys are pure ascii now.

3.2.0 (2016-10-29)
------------------

* Changed the signal key cleanup operation do be done without any expires. This prevents lingering keys around for some time.
  Contributed by Andrew Pashkin in `#38 <https://github.com/ionelmc/python-redis-lock/pull/38>`_.
* Allow locks with given `id` to acquire. Previously it assumed that if you specify the `id` then the lock was already
  acquired. See `#44 <https://github.com/ionelmc/python-redis-lock/issues/44>`_ and
  `#39 <https://github.com/ionelmc/python-redis-lock/issues/39>`_.
* Allow using other redis clients with a ``strict=False``. Normally you're expected to pass in an instance
  of ``redis.StrictRedis``.
* Added convenience method `locked_get_or_set` to Django cache backend.

3.1.0 (2016-04-16)
------------------

* Changed the auto renewal to automatically stop the renewal thread if lock gets garbage collected. Contributed by
  Andrew Pashkin in `#33 <https://github.com/ionelmc/python-redis-lock/pull/33>`_.

3.0.0 (2016-01-16)
------------------

* Changed ``release`` so that it expires signal-keys immediately. Contributed by Andrew Pashkin in `#28
  <https://github.com/ionelmc/python-redis-lock/pull/28>`_.
* Resetting locks (``reset`` or ``reset_all``) will release the lock. If there's someone waiting on the reset lock now it will
  acquire it. Contributed by Andrew Pashkin in `#29 <https://github.com/ionelmc/python-redis-lock/pull/29>`_.
* Added the ``extend`` method on ``Lock`` objects. Contributed by Andrew Pashkin in `#24
  <https://github.com/ionelmc/python-redis-lock/pull/24>`_.
* Documentation improvements on ``release`` method. Contributed by Andrew Pashkin in `#22
  <https://github.com/ionelmc/python-redis-lock/pull/22>`_.
* Fixed ``acquire(block=True)`` handling when ``expire`` option was used (it wasn't blocking indefinitely). Contributed by
  Tero Vuotila in `#35 <https://github.com/ionelmc/python-redis-lock/pull/35>`_.
* Changed ``release`` to check if lock was acquired with he same id. If not, ``NotAcquired`` will be raised.
  Previously there was just a check if it was acquired with the same instance (self._held).
  **BACKWARDS INCOMPATIBLE**
* Removed the ``force`` option from ``release`` - it wasn't really necessary and it only encourages sloppy programming. See
  `#25 <https://github.com/ionelmc/python-redis-lock/issues/25>`_.
  **BACKWARDS INCOMPATIBLE**
* Dropped tests for Python 2.6. It may work but it is unsupported.

2.3.0 (2015-09-27)
------------------

* Added the ``timeout`` option. Contributed by Victor Torres in `#20 <https://github.com/ionelmc/python-redis-lock/pull/20>`_.

2.2.0 (2015-08-19)
------------------

* Added the ``auto_renewal`` option. Contributed by Nick Groenen in `#18 <https://github.com/ionelmc/python-redis-lock/pull/18>`_.

2.1.0 (2015-03-12)
------------------

* New specific exception classes: ``AlreadyAcquired`` and ``NotAcquired``.
* Slightly improved efficiency when non-waiting acquires are used.

2.0.0 (2014-12-29)
------------------

* Rename ``Lock.token`` to ``Lock.id``. Now only allowed to be set via constructor. Contributed by Jardel Weyrich in `#11 <https://github.com/ionelmc/python-redis-lock/pull/11>`_.

1.0.0 (2014-12-23)
------------------

* Fix Django integration. (reported by Jardel Weyrich)
* Reorganize tests to use py.test.
* Add test for Django integration.
* Add ``reset_all`` functionality. Contributed by Yokotoka in `#7 <https://github.com/ionelmc/python-redis-lock/pull/7>`_.
* Add ``Lock.reset`` functionality.
* Expose the ``Lock.token`` attribute.

0.1.2 (2013-11-05)
------------------

* ?

0.1.1 (2013-10-26)
------------------

* ?

0.1.0 (2013-10-26)
------------------

* ?

0.0.1 (2013-10-25)
------------------

* First release on PyPI.
