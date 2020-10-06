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
import { TemplateHelperService } from '../../../services/template-helper.service';


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
  index = 1;
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
  public defaultTemplateData: any = {};
  readonly VARIABLES = 'variables';
  public typesInSources: any[] = [];

  private sourceTypes: any[];
  // receives data from the sources step
  @Input() set sources(value: any[]) {
    this.sourceTypes = value;
  }

  get sources(): any[] {
    return this.sourceTypes;
  }

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

    this.typeService.getTypeList().subscribe(resp => {
      this.typeList = resp;
    });
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

  public onOptionSelected(index, value) {
    // gets template helper data of the given object and inserts it at the specified index of this.templatehelperdata
    this.templateHelperService.getObjectTemplateHelperData(value).then(helperData => {
      this.templateHelperData[index] = helperData;
    });
  }

  public setTemplateValue(index, value, variable) {
    // sets the text of the specified input field and validates the field in the form
    (document.getElementById('input-' + index) as HTMLInputElement).value = value;
    variable.patchValue({
      template: value
    });
  }

  public setDefaultValue(index, value, variable) {
    // sets the text of the specified input field and validates the field in the form
    (document.getElementById('variableDefault' + index) as HTMLInputElement).value = value;
    variable.patchValue({
      default: value
    });
  }

  public determineDropDownDirection() {
    // determines what direction the dropdowns will be facing
    function determine() {
      $('.dropdown-menu').each(function() {

        // Invisibly expand the dropdown menu so its true height can be calculated
        $(this).css({
          visibility: 'hidden',
          display: 'block'
        });

        // Necessary to remove class each time so we don't unwantedly use dropup's offset top
        $(this).parent().removeClass('dropup');
        $(this).removeClass('dropdown-menu-right').removeClass('dropdown-menu-left');

        // Determine whether bottom of menu will be below window at current scroll position
        if ($(this).offset().top + $(this).outerHeight() > $(window).innerHeight() + $(window).scrollTop() + 10) {
          $(this).parent().addClass('dropup');
        }

        // Determine whether the right of menu will be outside of window at current scroll position
        if ($(this).offset().left + $(this).outerWidth() > $(window).innerWidth() + $(window).scrollLeft()) {
          $(this).addClass('dropdown-menu-left');
        } else {
          $(this).addClass('dropdown-menu-right');
        }

        // Return dropdown menu to fully hidden state
        $(this).css( {
        visibility: '', display: ''
        });
      });
    }

    determine();
  }

  private filterTypes() {
    // gets all type IDs from the data received form sources
    const typeArray = [];
    this.sources.forEach( source => {
      if (!typeArray.includes(source.type_id)) {
        typeArray.push(source.type_id);
      }
    });
    // filters all duplicates and gets the respective template helper data of the given types
    this.typesInSources = [];
    this.typeList.forEach( item => {
      if (typeArray.includes(item.public_id) && !this.typesInSources.includes(item)) {
        this.typesInSources.push(item);
        this.templateHelperService.getObjectTemplateHelperData(item.public_id).then(helperData => {
          this.defaultTemplateData[item.public_id] = helperData;
        });
      }
    });
  }

  private isID(field) {
    // used to determine wether the field calling it is the first in the list where the Public ID is located
    if (field === 0) {
      return 'fas fa-list-ol';
    } else {
      return 'fas fa-code';
    }
  }

}
