from distutils.core import setup
setup(
  name = 'thereporter', 
  packages = ['thereporter'],
  version = '0.1',
  license='MIT',
  description = 'Telegram bot interface for bug report', 
  author = 'Nikita',
  author_email = 'kutuku62@gmail.com',
  url = 'https://github.com/nikitos4319/TheReporter',
  keywords = ['BUG', 'REPORT', 'TELEGRAM', 'BOT'],
  install_requires=[
    'requests',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3', 
  ],
)