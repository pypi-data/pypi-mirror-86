from setuptools import setup, find_packages 
  
long_description = 'Traceroute with Python for Windows & Linux'
  
setup( 
        name ='traceroute-imt', 
        version ='1.5.0', 
        author ='Javed & Emeric', 
        author_email ='jsyedk@gmail.com', 
        description ='Traceroute with Python for Windows and Linux', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'traceroute-imt = traceroute_win.traceroute_win:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='traceroute python package windows linux fastjaved', 
        install_requires = ["scapy", "requests", "progressbar"], 
        zip_safe = False
) 
