import { FormGroup } from '@angular/forms';
import { Input } from '@angular/core';

export class FileConfig {
  @Input() defaultParserConfig: any = {};
  public configForm: FormGroup;

  public constructor() {
    this.configForm = new FormGroup({});
  }

}
