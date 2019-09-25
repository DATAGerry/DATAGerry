import { Component, OnInit, ViewChild } from '@angular/core';
import { ImportService } from '../import.service';
import { SelectFileComponent } from './select-file/select-file.component';
import { Subject } from 'rxjs';
import { CmdbType } from '../../framework/models/cmdb-type';
import { FileConfigComponent } from './file-config/file-config.component';
import { SelectTypeComponent } from './select-type/select-type.component';

@Component({
  selector: 'cmdb-import-objects',
  templateUrl: './import-objects.component.html',
  styleUrls: ['./import-objects.component.scss']
})
export class ImportObjectsComponent implements OnInit {

  @ViewChild(SelectFileComponent, { static: true })
  public selectFileComponent: SelectFileComponent;

  @ViewChild(FileConfigComponent, { static: true })
  public fileConfigComponent: FileConfigComponent;

  @ViewChild(SelectTypeComponent, { static: true })
  public selectTypeComponent: SelectTypeComponent;

  public previewTrigger: Subject<any>;
  private fileReader: FileReader;

  public file: File;
  public fileContent: string | ArrayBuffer = undefined;
  public fileFormat: string = undefined;
  public typeInstance: CmdbType = undefined;
  public defaultParserConfig: any = {};
  public parserConfig: any = {};

  constructor(private importerService: ImportService) {
    this.fileReader = new FileReader();
    this.previewTrigger = new Subject<any>();
  }

  public ngOnInit(): void {
    this.fileReader.onload = (e) => {
      this.fileContent = this.fileReader.result;
    };
  }

  public formatChange(format: string) {
    this.fileFormat = format;
    this.importerService.getObjectParserDefaultConfig(this.fileFormat).subscribe(defaults => {
      this.defaultParserConfig = defaults;
    });
  }

  public fileChange(file: File) {
    this.file = file;
    this.fileReader.readAsText(file);
  }

  public typeChange(typeInstance: CmdbType) {
    this.typeInstance = typeInstance;
  }

  public configExit() {
    this.parserConfig = this.fileConfigComponent.configForm.getRawValue();
  }

  public typeSelectExit() {
    this.previewTrigger.next(this.parserConfig);
  }

}
