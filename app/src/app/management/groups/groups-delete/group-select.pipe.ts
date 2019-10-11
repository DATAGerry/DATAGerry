import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'groupSelect',
  pure: true
})
export class GroupSelectPipe implements PipeTransform {

  public transform(items: any[], publicID: number): any {
    if (items === undefined) {
      return [];
    }
    return items.filter(item => {
      return item.public_id !== +publicID;
    });
  }

}
