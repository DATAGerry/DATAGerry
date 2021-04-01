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

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ConfigEditBaseComponent } from '../config.edit';
import { CmdbType, CmdbTypeSection } from '../../../../models/cmdb-type';
import { CollectionParameters } from '../../../../../services/models/api-parameter';
import { TypeService } from '../../../../services/type.service';
import { takeUntil } from 'rxjs/operators';
import { APIGetMultiResponse } from '../../../../../services/models/api-response';
import { RenderResult } from '../../../../models/cmdb-render';
import { ReplaySubject } from 'rxjs';
import { CmdbMode } from '../../../../modes.enum';

@Component({
  selector: 'cmdb-section-ref-field-edit',
  templateUrl: './section-ref-field-edit.component.html',
  styleUrls: ['./section-ref-field-edit.component.scss']
})
export class SectionRefFieldEditComponent extends ConfigEditBaseComponent implements OnInit, OnDestroy {

  /**
   * Component un subscriber.
   * @private
   */
  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();

  /**
   * Sections from the selected type.
   */
  public typeSections: Array<CmdbTypeSection> = [];

  /**
   * Selected section
   */
  public selectedSection: CmdbTypeSection;

  /**
   * Types load right now?
   */
  public loading: boolean = false;

  /**
   * Total number of types.
   */
  public totalTypes: number = 0;

  /**
   * Current loading page
   * @private
   */
  private currentPage: number = 1;

  /**
   * Max loading pages.
   * @private
   */
  private maxPage: number = 1;

  /**
   * Type switch active.
   */
  public selectDisabled: boolean = false;

  @Input('data')
  public set Data(value: CmdbTypeSection) {
    if (value?.reference?.type_id) {
      this.loadPresetType(value.reference.type_id);
    }
    this.data = value;
  }

  constructor(private typeService: TypeService) {
    super();
  }

  /**
   * Generate the type call parameters
   * @param page
   * @private
   */
  static getApiParameters(page: number = 1): CollectionParameters {
    return {
      filter: undefined, limit: 10, sort: 'public_id',
      order: 1, page
    } as CollectionParameters;
  }

  public ngOnInit(): void {
    this.triggerAPICall();
  }

  private loadPresetType(publicID: number): void {
    this.loading = true;
    this.typeService.getType(publicID).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: CmdbType) => {
        this.types = [...this.types, ...[apiResponse as CmdbType]];
      }).add(() => this.loading = false);
  }

  private triggerAPICall(): void {
    if (this.maxPage && (this.currentPage <= this.maxPage)) {
      this.loadTypesFromApi();
      this.currentPage += 1;
    }
  }

  private loadTypesFromApi(): void {
    this.loading = true;
    this.typeService.getTypes(SectionRefFieldEditComponent.getApiParameters(this.currentPage)).pipe(takeUntil(this.subscriber))
      .subscribe((apiResponse: APIGetMultiResponse<CmdbType>) => {
        this.types = [...this.types, ...apiResponse.results as Array<CmdbType>];
        this.totalTypes = apiResponse.total;
        this.maxPage = apiResponse.pager.total_pages;
      }).add(() => this.loading = false);
  }

  public onScrollToEnd(): void {
    this.triggerAPICall();
  }

  /**
   * When the selected type change.
   * Reset a selected section.
   * @param type
   */
  public onTypeChange(type: CmdbType): void {
    if (this.data.reference.section_name) {
      this.data.reference.section_name = undefined;
      this.data.reference.selected_fields = undefined;
      this.selectedSection = undefined;
    }
    this.typeSections = this.getSectionsFromType(type.public_id);
  }

  /**
   * Get all sections from a type.
   * @param typeID
   */
  public getSectionsFromType(typeID: number): Array<CmdbTypeSection> {
    return this.types.find(t => t.public_id === typeID).render_meta.sections;
  }

  /**
   * When section selection changed.
   * @param section
   */
  public onSectionChange(section: CmdbTypeSection): void {
    this.selectedSection = section;
    this.data.reference.selected_fields = undefined;
  }

  /**
   * Change the field when the reference changes
   * @param name
   */
  public onNameChange(name: string) {
    const oldName = this.data.name;
    const fieldIdx = this.data.fields.indexOf(`${ oldName }-field`);
    const field = this.fields.find(x => x.name === `${ oldName }-field`);
    this.data.fields[fieldIdx] = `${ name }-field`;
    field.name = `${ name }-field`;
  }

  /**
   * Destroy component.
   */
  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }

}
