/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import {Component, Directive, Input, OnInit, Pipe, PipeTransform, HostListener} from '@angular/core';
import { CmdbMode } from '../../../../framework/modes.enum';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbType } from '../../../../framework/models/cmdb-type';
import { TypeService } from '../../../../framework/services/type.service';
import { ExportdJobDestinationsStepComponent } from '../exportd-job-destinations-step/exportd-job-destinations-step.component';
import { ExternalSystemService } from '../../../services/external_system.service';
import { DndDropEvent, DropEffect } from 'ngx-drag-drop';
import {TemplateHelperService} from '../../../services/template-helper.service';

@Directive(
  {
    selector: '[cmdbTest]'
  })
export class HostDirective {
  @HostListener('mouseover', ['$event']) onClick(event: Event) {
    console.log(event);
  }
}

@Pipe({
  name: 'filterUnique',
  pure: false
})
export class FilterPipe implements PipeTransform {

  transform(value: any, args?: any): any {
    const newArr = [];
    value.forEach((item, index) => {
      if (newArr.findIndex(i => i.className === item.className) === -1) {
        newArr.push(item);
      }
    });
    return newArr;
  }
}

@Component({
  selector: 'cmdb-task-variables-step',
  templateUrl: './exportd-job-variables-step.component.html',
  styleUrls: ['./exportd-job-variables-step.component.scss']
})
export class ExportdJobVariablesStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.variables) {
        // Create variables
        this.variableForm = this.formBuilder.group({
          variables: new FormArray([])
        });
        this.variableForm.removeControl('variables');
        const forArray: FormArray = this.formBuilder.array([]);
        let i = 0;
        while (i < data.variables.length) {
          forArray.push(this.formBuilder.group({
            name: new FormControl('', Validators.required),
            default: new FormControl('', Validators.required),
            templates: this.formBuilder.array([])
          }));
          i++;
        }

        // Create templates
        i = 0;
        while (i < forArray.controls.length) {
          for (const item of data.variables[i].templates) {
            const control = forArray.controls[i].get('templates') as FormArray;
            control.push(this.createTemplate());
          }
          i++;
        }

        this.variableForm.addControl('variables', forArray);
        this.variableForm.patchValue(data);
      }
    }
  }

  private destinationForm: ExportdJobDestinationsStepComponent;
  @Input() public mode: CmdbMode;
  public typeList: CmdbType[] = [];
  public variableForm: FormGroup;
  public variableHelper: any[];
  public dragVariableName: string = '';
  public templateHelperData: any = {};
  readonly VARIABLES = 'variables';


  constructor(private formBuilder: FormBuilder, private typeService: TypeService,
              private externalService: ExternalSystemService, private templateHelperService: TemplateHelperService) {
  }

  @Input() set destinationStep(value: ExportdJobDestinationsStepComponent) {
    this.destinationForm = value;
  }

  get destinationStep(): ExportdJobDestinationsStepComponent {
    return this.destinationForm;
  }

  ngOnInit() {
    this.variableForm = this.formBuilder.group({
      variables: this.formBuilder.array([this.createVariable()])
    });
    this.typeService.getTypeList().subscribe((value: CmdbType[]) => this.typeList = value);
  }

  private createVariable(): FormGroup {
    return this.formBuilder.group({
      name: new FormControl('', Validators.required),
      default: new FormControl('', Validators.required),
      templates: this.formBuilder.array([this.createTemplate()])
    });
  }

  private createTemplate(): FormGroup {
    return this.formBuilder.group({
      type: new FormControl('', Validators.required),
      template: new FormControl('', Validators.required)
    });
  }

  private getVariableAsFormArray(): any {
    return this.variableForm.controls[this.VARIABLES] as FormArray;
  }

  public addVariable(): void {
    const control = this.getVariableAsFormArray();
    control.push(this.createVariable());
  }

  public addTemplate(event): void {
    const control = this.getVariableAsFormArray().at(event).get('templates') as FormArray;
    control.push(this.createTemplate());
  }

  public delVariable(index): void {
    const control = this.getVariableAsFormArray();
    control.removeAt(index);
  }

  public delTemplate(index, event): void {
    const control = this.getVariableAsFormArray().at(event).get('templates') as FormArray;
    control.removeAt(index);
    if (this.templateHelperData[index]) {
      delete this.templateHelperData[index];
    }
  }

  public getVariableHelp(value: string) {
    this.externalService.getExternSytemVariables(value).subscribe(item => {
      this.variableHelper = item;
    });
  }

  public onDrop(item: DndDropEvent) {
    const group = this.getVariableAsFormArray().at(item.data.oldIndex);
    this.getVariableAsFormArray().removeAt(item.data.oldIndex);
    this.getVariableAsFormArray().insert(item.index, group);
  }

  public onDndStart(name: string) {
    this.dragVariableName = name;
  }

  public getCmdbDataMenuItems(editor) {
    const items = [];
    items.push({
      type: 'nestedmenuitem',
      text: 'Object Template Data',
      icon: 'code-sample',
      getSubmenuItems: () => {
        return this.getObjectDataMenuItems(editor);
      }
    });
    return items;
  }

  public getObjectDataMenuItems(editor, templateHelperData = this.templateHelperData) {
    const items = [];
    for (const item of templateHelperData) {
      if (item.subdata) {
        items.push({
          type: 'nestedmenuitem',
          text: item.label,
          icon: 'chevron-right',
          getSubmenuItems: () => {
            return this.getObjectDataMenuItems(editor, item.subdata);
          }
        });
      } else {
        let icon = 'sourcecode';
        if (item.label === 'Public ID') {
          icon = 'character-count';
        }
        items.push({
          type: 'menuitem',
          text: item.label,
          icon,
          onAction() {
            editor.insertContent(item.templatedata);
          }
        });
      }
    }
  }

  public onOptionSelected(index, value) {
    console.log(index + ' ' + value);
    this.templateHelperService.getObjectTemplateHelperData(value).then(helperData => {
      this.templateHelperData[index] = helperData;
      console.log(helperData);
    });
    console.log(this.templateHelperData[index]);
  }
}
