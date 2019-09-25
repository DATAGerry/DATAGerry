import { Input } from '@angular/core';
import { CmdbType } from '../../../framework/models/cmdb-type';

export class FilePreview {

  @Input() public config: {};
  @Input() public file: File;
  @Input() public fileFormat: string;
  @Input() public typeInstance: CmdbType;

  public constructor() {

  }

}
