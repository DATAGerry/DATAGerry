import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'mappingControl',
  pure: false
})
export class MappingControlPipe implements PipeTransform {

  transform(items: [], idx: string, value: string): any {
    if (!items || !idx) {
      return items;
    }
    return items.filter(item => item[idx] === value);
  }

}
