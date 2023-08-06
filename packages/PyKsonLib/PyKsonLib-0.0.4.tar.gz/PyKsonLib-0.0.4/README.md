Currently works with KTHS-415BS only,write program function can only write
two steps with 1 target temp&humidity for normal use.

Coding Example:
```
from PyKsonLib.models import KTHS_415BS

if __name__ == '__main__':
    p = KTHS_415BS("/dev/ttyUSB0")
    p.get_status()
    p.delete_pgm('bbb.pgm')
    print(p.pgm_jump_section(2))
    print(p.pgm_jump_next())
    p.list_all_pgm()
    p.load_pgm('-40.pgm')
    p.rename_pgm('162.pgm', '162r.pgm')
    p.view_pgm('-40.pgm')
    p.run_loaded_pgm()
    p.execute_pgm('90.pgm')
    p.write_pgm(pgm_name="lt.pgm", target_temp=25, target_humi=50, target_hour=2000, target_min=0)

```