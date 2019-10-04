import { Component, OnDestroy, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  selector: 'cmdb-export-types-config-step',
  templateUrl: './export-types-config-step.component.html',
  styleUrls: ['./export-types-config-step.component.scss']
})
export class ExportTypesConfigStepComponent implements OnInit, OnDestroy {

  public readonly defaultExportFormat: string = 'json';
  public readonly defaultConfig: any[] = [
    {
      property: 'active',
      label: 'Active',
      value: true,
      options: []
    },
    {
      property: 'public_id',
      label: 'Public ID',
      value: false,
      options: []
    },
    {
      property: 'name',
      label: 'name',
      value: true,
      options: []
    },
    {
      property: 'label',
      label: 'label',
      value: true,
      options: []
    },
    {
      property: 'description',
      label: 'Description',
      value: true,
      options: []
    },
    {
      property: 'access',
      label: 'Access',
      value: true,
      options: []
    },
    {
      property: 'render_meta',
      label: 'Render Meta',
      value: true,
      options: [{
        property: 'summary',
        label: 'Summary',
        value: true,
      }, {
        property: 'external',
        label: 'External',
        value: true,
      }, {
        property: 'sections',
        label: 'Sections',
        value: true,
      }]
    },
    {
      property: 'fields',
      label: 'Fields',
      value: true,
      options: []
    },
  ];
  public fileFormatForm: FormGroup;
  public configForm: FormGroup;
  public properties: FormGroup;
  public options: FormGroup;

  constructor() {
    this.fileFormatForm = new FormGroup({
      fileFormat: new FormControl(this.defaultExportFormat, Validators.required),
    });

    this.properties = new FormGroup({});
    this.options = new FormGroup({});
    for (const property of this.defaultConfig) {
      this.properties.addControl(property.property, new FormControl(property.value));
      if (property.options.length > 0) {
        this.options.addControl(property.property, new FormControl(''));
      }
    }
    this.configForm = new FormGroup({ properties: this.properties, options: this.options });

  }

  private get fileFormat(): AbstractControl {
    return this.fileFormatForm.get('fileFormat');
  }

  public get propertiesControls() {
    return this.properties.controls;
  }

  public ngOnInit(): void {
    this.fileFormat.disable({ onlySelf: true });
  }

  public ngOnDestroy(): void {

  }

}
