/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import {
  Component,
  Directive,
  ElementRef,
  HostListener,
  Input, OnDestroy,
  OnInit,
  Pipe,
  PipeTransform,
  Renderer2
} from '@angular/core';
import { CmdbMode } from '../../../framework/modes.enum';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbType } from '../../../framework/models/cmdb-type';
import { TypeService } from '../../../framework/services/type.service';
import { ExportdJobDestinationsStepComponent } from '../exportd-job-destinations-step/exportd-job-destinations-step.component';
import { ExternalSystemService } from '../../../settings/services/external-system.service';
import { DndDropEvent } from 'ngx-drag-drop';
import { TemplateHelperService } from '../../../settings/services/template-helper.service';
import { ExportdJobBaseStepComponent } from '../exportd-job-base-step.component';
import { BehaviorSubject, Observable, ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';


@Directive({
  // tslint:disable-next-line:directive-selector
  selector: '[dropdowndirection]'
})
export class DropDownDirectionDirective {


  constructor(private el: ElementRef, private renderer: Renderer2) {
  }

  // listens to the mouseenter event on the element this directive is called
  @HostListener('mouseenter', ['$event.target'])
  determineDirection(target): void {
    for (const child of target.children) {

      // checks if the child is a dropdow menu
      if (child.className.includes('dropdown-menu')) {

        // displays the dropdown menu in a hidden state to determine how it would be positioned
        this.renderer.setStyle(child, 'visibility', 'hidden');
        this.renderer.setStyle(child, 'display', 'block');

        // removes all classes to prevent wrong data to be compared
        this.renderer.removeClass(child, 'dropdown-menu-left');
        this.renderer.removeClass(child, 'dropdown-menu-right');
        this.renderer.removeClass(child.parentNode, 'dropup');

        // if the menu will be displayed under the window border it will be turned into a dropup
        // except if it would be displayed above the upper window border
        if (($(child).offset().top + $(child).outerHeight() > window.innerHeight + window.scrollY + 10)
          && ($(child).offset().top - $(child).outerHeight()) > 90) {
          this.renderer.addClass(child.parentNode, 'dropup');
        }

        // Determines if the menu would display outside of the right border and adjust its position
        if ($(child).offset().left + $(child).outerWidth() + 200 > window.innerWidth + window.scrollX) {
          this.renderer.addClass(child, 'dropdown-menu-left');
        } else {
          this.renderer.addClass(child, 'dropdown-menu-right');
        }

        // Returns the menu to its original state
        this.renderer.removeStyle(child, 'visibility');
        this.renderer.removeStyle(child, 'display');
      }

    }
  }

}

@Pipe({
  name: 'filterUnique',
  pure: false
})
export class FilterPipe implements PipeTransform {

  transform(value: any, args?: any): any {
    const newArr = [];
    value.forEach((item) => {
      if (newArr.findIndex(i => i.className === item.className) === -1) {
        newArr.push(item);
      }
    });
    return newArr;
  }
}

// @ts-ignore
@Component({
  selector: 'cmdb-task-variables-step',
  templateUrl: './exportd-job-variables-step.component.html',
  styleUrls: ['./exportd-job-variables-step.component.scss']
})
export class ExportdJobVariablesStepComponent extends ExportdJobBaseStepComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public index: number = 1;

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.variables) {
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

        i = 0;
        while (i < forArray.controls.length) {
          data.variables[i].templates.forEach((item, index) => {
            const control = forArray.controls[i].get('templates') as FormArray;
            control.push(this.createTemplate());
            this.onOptionSelected(i, index, item.type);
          });
          i++;
        }

        this.variableForm.addControl('variables', forArray);
        this.variableForm.patchValue(data);
      }
    }
  }

  private destinationForm: ExportdJobDestinationsStepComponent;

  public variableForm: FormGroup;
  public variableHelper: any[];
  public dragVariableName: string = '';
  public templateHelperData: any = {};
  public defaultTemplateData: any = {};
  readonly VARIABLES = 'variables';
  public typesInSources: any[] = [];

  private sourceTypes: any[];

  @Input() set sources(value: any[]) {
    this.sourceTypes = value;
  }

  get sources(): any[] {
    return this.sourceTypes;
  }

  constructor(private formBuilder: FormBuilder, private externalService: ExternalSystemService,
              private templateHelperService: TemplateHelperService, private typeService: TypeService) {
    super();
  }

  @Input() set destinationStep(value: ExportdJobDestinationsStepComponent) {
    this.destinationForm = value;
  }

  get destinationStep(): ExportdJobDestinationsStepComponent {
    return this.destinationForm;
  }

  public ngOnInit(): void {
    this.variableForm = this.formBuilder.group({
      variables: this.formBuilder.array([this.createVariable()])
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
    if (this.templateHelperData[event][index]) {
      delete this.templateHelperData[event][index];
    }
  }

  public getVariableHelp(value: string) {
    this.externalService.getExternSystemVariables(value).pipe(takeUntil(this.subscriber)).subscribe(item => {
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

  /**
   * gets template helper data of the given object and inserts it at the specified index of this.templatehelperdata
   * @param superindex
   * @param index
   * @param value
   */
  public onOptionSelected(superindex, index, value) {
    this.templateHelperService.getObjectTemplateHelperData(value).then(helperData => {
      this.templateHelperData[superindex][index] = helperData;
    });
  }

  /**
   * used to determine whether the an array exists in the superindex and returns it or an empty array
   * @param superindex
   * @param index
   */
  public getTemplateHelperData(superindex, index) {
    if (!this.templateHelperData[superindex]) {
      this.templateHelperData[superindex] = [];
    }
    return this.templateHelperData[superindex][index];
  }

  /**
   * sets the text of the specified input field and validates the field in the form
   * @param superindex
   * @param index
   * @param value
   * @param variable
   */
  public setTemplateValue(superindex, index, value, variable) {
    const element = (document.getElementById('input' + superindex + index) as HTMLInputElement);
    element.value = element.value + value;
    variable.patchValue({
      template: element.value
    });
  }

  /**
   * sets the text of the specified input field and validates the field in the form
   * @param index
   * @param value
   * @param variable
   */
  public setDefaultValue(index, value, variable) {
    const element = (document.getElementById('variableDefault' + index) as HTMLInputElement);
    element.value = element.value + value;
    variable.patchValue({
      default: element.value
    });
  }

  public filterTypes() {
    const typeArray = [];
    this.sources.forEach(source => {
      if (!typeArray.includes(source.type_id)) {
        typeArray.push(source.type_id);
      }
    });
    this.typesInSources = [];
    this.types.forEach(item => {
      if (typeArray.includes(item.public_id) && !this.typesInSources.includes(item)) {
        this.typesInSources.push(item);
        this.templateHelperService.getObjectTemplateHelperData(item.public_id).then(helperData => {
          this.defaultTemplateData[item.public_id] = helperData;
        });
      }
    });
  }

  /**
   * used to determine wether the field calling it is the first in the list where the Public ID is located
   * @param field
   */
  public isID(field) {
    if (field === 0) {
      return 'fas fa-list-ol';
    } else {
      return 'fas fa-code';
    }
  }

  /**
   * Load types to display
   * @param publicID
   */
  public loadDisplayType(publicID: number): Observable<CmdbType> {
    const foundType = this.types.find(f => f.public_id === publicID);
    if (foundType) {
      return new BehaviorSubject<CmdbType>(foundType).asObservable();
    }
    return this.typeService.getType(publicID).pipe(takeUntil(this.subscriber));
  }

  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }
}
