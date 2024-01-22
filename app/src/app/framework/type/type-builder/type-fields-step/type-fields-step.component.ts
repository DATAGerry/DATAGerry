/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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
*
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/
import { Component, DoCheck, Input, KeyValueDiffer, KeyValueDiffers, OnDestroy, OnInit } from '@angular/core';

import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { SectionTemplateService } from 'src/app/framework/section_templates/services/section-template.service';

import { TypeBuilderStepComponent } from '../type-builder-step.component';
import { CmdbType } from '../../../models/cmdb-type';
import { CmdbSectionTemplate } from 'src/app/framework/models/cmdb-section-template';
import { APIGetMultiResponse } from 'src/app/services/models/api-response';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
  selector: 'cmdb-type-fields-step',
  templateUrl: './type-fields-step.component.html',
  styleUrls: ['./type-fields-step.component.scss']
})
export class TypeFieldsStepComponent extends TypeBuilderStepComponent implements OnInit, DoCheck, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();
  private typeInstanceDiffer: KeyValueDiffer<string, any>;

  public sectionTemplates: Array<CmdbSectionTemplate> = [];
  public globalSectionTemplates: Array<CmdbSectionTemplate> = [];

  public builderValid: boolean = true;

  @Input('typeInstance')
  public set TypeInstance(instance: CmdbType) {
    if (instance) {
      this.typeInstance = instance;
      this.typeInstanceDiffer = this.differs.find(this.typeInstance).create();
    }
  }

/* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */
    public constructor(private differs: KeyValueDiffers, private sectionTemplateService: SectionTemplateService) {
        super();
    }


    public ngOnInit(): void {
        this.typeInstanceDiffer = this.differs.find(this.typeInstance).create();
          this.getAllSectionTemplates();

    }


    public ngDoCheck(): void {
        const changes = this.typeInstanceDiffer.diff(this.typeInstance);
        if (changes) {
            this.valid = this.status;
            this.validateChange.emit(this.valid);
        }
      }


    public ngOnDestroy(): void {
        this.subscriber.next();
        this.subscriber.complete();
    }

/* ---------------------------------------------------- FUCNTIONS --------------------------------------------------- */

    public get status(): boolean{
        const hasFields: boolean = this.typeInstance.fields.length > 0;
        const hasSections: boolean = this.typeInstance.render_meta.sections.length > 0;

        return hasFields && hasSections && this.builderValid;
    }


    public onBuilderValidChange(status: boolean): void{
        this.builderValid = status;
        this.valid = this.status;
        this.validateChange.emit(this.valid);
    }


    private getAllSectionTemplates(){
        this.sectionTemplateService.getSectionTemplates().pipe(takeUntil(this.unsubscribe))
        .subscribe((apiResponse: APIGetMultiResponse<CmdbSectionTemplate>) => {
            this.sectionTemplates = apiResponse.results.filter((template) => template.is_global == false);
            this.globalSectionTemplates = apiResponse.results.filter((template) => template.is_global == true);
        });
    }
}
