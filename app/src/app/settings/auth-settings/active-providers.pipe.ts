import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'activeProviders',
  pure: false
})
export class ActiveProvidersPipe implements PipeTransform {

  transform(value: any, ...args: any[]): any {
    const activeProviderList: any[] = [];
    for (const provider of value) {
      if (provider.config.active) {
        activeProviderList.push(provider);
      }
    }
    return activeProviderList;
  }

}
