import { Component, Input, OnInit, OnChanges, SimpleChanges, Output, EventEmitter, OnDestroy } from '@angular/core';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { FormArray, FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'cmdb-export-types-select-step',
  templateUrl: './export-types-select-step.component.html',
  styleUrls: ['./export-types-select-step.component.scss']
})
export class ExportTypesSelectStepComponent implements OnInit, OnChanges, OnDestroy {

  @Input() typeList: CmdbType[];
  @Output() typeSelectionEmitter: EventEmitter<boolean[]>;
  public selectTypeForm: FormGroup;

  public constructor() {
    this.typeSelectionEmitter = new EventEmitter<boolean[]>();
  }

  public ngOnInit(): void {
    this.selectTypeForm = new FormGroup({
      types: new FormArray([])
    });
  }

  public get typeArray(): FormArray {
    return (this.selectTypeForm.get('types') as FormArray);
  }

  public ngOnChanges(changes: SimpleChanges): void {
    if (changes.typeList.currentValue !== undefined && changes.typeList.firstChange !== true) {
      this.selectTypeForm.reset();
      for (const typeInstance of this.typeList) {
        this.typeArray.push(new FormControl(false));
      }
    }
  }

  public selectAll(checked): void {
    for (const typeControl of this.typeArray.controls) {
      typeControl.setValue(checked);
    }
  }

  public emitSelection() {
    this.typeSelectionEmitter.emit(this.typeArray.getRawValue());
  }

  public ngOnDestroy(): void {
    this.typeSelectionEmitter.complete();
  }

}
