import { Component, Input, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';


@Component({
  selector: 'cmdb-type-meta-step',
  templateUrl: './type-meta-step.component.html',
  styleUrls: ['./type-meta-step.component.scss']
})
export class TypeMetaStepComponent implements OnInit {

  public summaryForm: FormGroup;
  public externalsForm: FormGroup;
  public externalLinks = [];
  public hrefInterpolCounter;
  private currentFields: any[] = [];
  private currentSummaries: any[] = [];

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      if (data.render_meta !== undefined) {
        this.summaryForm.patchValue(data.render_meta.summary);
        this.externalLinks = data.render_meta.external;
      }
    }
  }

  constructor() {
    this.summaryForm = new FormGroup({
      fields: new FormControl('', Validators.required)
    });

    this.externalsForm = new FormGroup({
      name: new FormControl('', [Validators.required, this.listNameValidator(this.externalLinks)]),
      label: new FormControl('', Validators.required),
      icon: new FormControl(''),
      href: new FormControl('', [Validators.required]),
      fields: new FormControl('')
    });
  }

  public get external_name() {
    return this.externalsForm.get('name');
  }

  public get external_label() {
    return this.externalsForm.get('label');
  }

  @Input()
  public set fields(value: any[]) {
    const preFields = JSON.parse(JSON.stringify( value ));
    if (preFields != null) {
      preFields.push({label: 'Object ID', name: 'object_id'});
    }
    this.currentFields = preFields;
    this.currentSummaries = value;
    this.checkSummaryFields();
    this.checkExternalLinks();
  }

  public get fields(): any[] {
    return this.currentFields;
  }

  public get summaries(): any[] {
    return this.currentSummaries;
  }

  private static occurrences(s, subString): number {
    s += '';
    subString += '';
    if (subString.length <= 0) {
      return (s.length + 1);
    }

    let n = 0;
    let pos = 0;

    while (true) {
      pos = s.indexOf(subString, pos);
      if (pos >= 0) {
        ++n;
        pos += 1;
      } else {
        break;
      }
    }
    return n;
  }

  public listNameValidator(list: any[]) {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const nameInList = list.find(el => el.name === control.value);
      return nameInList ? {nameAlreadyTaken: {value: control.value}} : null;
    };
  }

  public ngOnInit(): void {

    this.externalsForm.get('name').valueChanges.subscribe(val => {
      if (this.externalsForm.get('name').value !== null) {
        this.externalsForm.get('label').setValue(val.charAt(0).toUpperCase() + val.toString().slice(1));
        this.externalsForm.get('label').markAsDirty({onlySelf: true});
        this.externalsForm.get('label').markAsTouched({onlySelf: true});
      }
    });

    this.externalsForm.get('href').valueChanges.subscribe((href: string) => {
      this.hrefInterpolCounter = Array(TypeMetaStepComponent.occurrences(href, '{}')).fill(0).map((x, i) => i);
    });
  }

  public addExternal() {
    this.externalLinks.push(this.externalsForm.value);
    this.externalsForm.reset();
    this.externalsForm.get('icon').setValue('fas fa-external-link-alt');
  }

  public editExternal(data) {
    const rawExternalData = this.externalLinks[this.externalLinks.indexOf(data)];
    this.externalsForm.reset();
    this.deleteExternal(data);
    this.externalsForm.patchValue(rawExternalData);
  }

  public deleteExternal(data) {
    const index: number = this.externalLinks.indexOf(data);
    if (index !== -1) {
      this.externalLinks.splice(index, 1);
    }
    this.externalsForm.get('name').clearValidators();
    this.externalsForm.get('name').setValidators(this.listNameValidator(this.externalLinks));
  }

  private checkSummaryFields() {
    // checking if summary-fields have removing fields
    const sumFields: any[] = this.summaryForm.get('fields').value;
    if (sumFields.length > 0) {
      const validList = [];
      sumFields.filter((item) => {
        this.summaries.map(field => field.name).includes(item) ? validList.push(item) : console.log(item);
      });
      this.summaryForm.patchValue({fields: validList});
    }
  }

  private checkExternalLinks() {
    // checking if external links have removing fields
    const extLinks: any[] = this.externalLinks;
    if (extLinks.length > 0) {
      let validList = [];
      extLinks.filter((item) => {
        if (item.fields.length > 0) {
          item.fields.filter((value) => {
            this.fields.map(field => field.name).includes(value) ? validList.push(value) : console.log(value);
          });
          item.fields = validList;
          validList = [];
        }
      });
    }
  }
}
