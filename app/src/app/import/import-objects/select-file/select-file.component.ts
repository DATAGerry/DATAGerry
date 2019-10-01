import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ImportService } from '../../import.service';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';

@Component({
  selector: 'cmdb-select-file',
  templateUrl: './select-file.component.html',
  styleUrls: ['./select-file.component.scss']
})
export class SelectFileComponent implements OnInit {

  private defaultFileFormat: string = '';
  public fileForm: FormGroup;
  public fileName: string = 'Choose file';
  public selectedFileFormat: string = `.${ this.defaultFileFormat }`;
  public importerTypes: string[] = [];

  @Output() public formatChange: EventEmitter<string>;
  @Output() public fileChange: EventEmitter<File>;

  public constructor(private importService: ImportService) {
    this.formatChange = new EventEmitter<string>();
    this.fileChange = new EventEmitter<File>();

    this.fileForm = new FormGroup({
      fileFormat: new FormControl(this.defaultFileFormat, Validators.required),
      file: new FormControl(null, Validators.required),
    });
  }

  public ngOnInit(): void {
    this.importService.getObjectImporters().subscribe((importerTypes: string[]) => {
      this.importerTypes = importerTypes;
    });

    this.fileForm.get('fileFormat').valueChanges.subscribe((format: string) => {
      this.formatChange.emit(format);
    });
    this.fileForm.get('file').valueChanges.subscribe((file) => {
      this.fileChange.emit(file);
    });
  }

  public get fileFormat() {
    return this.fileForm.get('fileFormat');
  }

  public selectFile(files) {
    if (files.length > 0) {
      const file = files[0];
      this.fileForm.get('file').setValue(file);
      this.fileName = file.name;
    }
  }

}
