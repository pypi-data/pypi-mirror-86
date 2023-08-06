Mysqldump is a django package used to generate
the logical backup of the MySQL database.

Installation

<ul>
    <li>
        <pre> <code> pip install mysqldump </code> </pre>
    </li>
    <li>
        <pre> Add <code>backupdb</code> to your settings.py </pre>
    </li>
    <li>
        <pre> Run the below command </pre> <br>
        <code> ./manage.py dumpdb </code>
    </li>
</ul>


setting.py
-------------- 

<h2> Installed Apps </h2>

<code>
    INSTALLED_APPS = [
    'backupdb',
]
</code>

<h2> TMP_DIR </h2>

To define custom temporary dir, if not django will use default system tmp directory