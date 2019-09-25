import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { FileConfig } from '../file-config';

@Component({
  templateUrl: './csv-config.component.html',
  styleUrls: ['./csv-config.component.scss']
})
export class CsvConfigComponent extends FileConfig implements OnInit {

  public constructor() {
    super();
  }

  public ngOnInit(): void {
    // tslint:disable-next-line:forin
    for (const defaultConfigEntry in this.defaultParserConfig) {
      this.configForm.addControl(defaultConfigEntry, new FormControl(''));
    }
    this.configForm.patchValue(this.defaultParserConfig);
  }

}
