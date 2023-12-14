/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2023 becon GmbH
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
import { Component, OnDestroy, OnInit } from '@angular/core';
import { SectionTemplateService } from './services/section-template.service';
import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';
import { RenderResult } from '../models/cmdb-render';
import { APIGetMultiResponse, APIUpdateSingleResponse } from 'src/app/services/models/api-response';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { SectionTemplateDeleteModalComponent } from './layout/modals/section-template-delete/section-template-delete-modal.component';
import { CmdbSectionTemplate } from '../models/cmdb-section-template';
import { ToastService } from 'src/app/layout/toast/toast.service';
import { Router } from '@angular/router';
import { SectionTemplateTransformModalComponent } from './layout/modals/section-template-transform/section-template-transform-modal.component';
/* ------------------------------------------------------------------------------------------------------------------ */

@Component({
    selector:'cmdb-section-template',
    templateUrl: './section-template.component.html',
    styleUrls: ['./section-template.component.scss']
})
export class SectionTemplateComponent implements OnInit, OnDestroy {
    public sectionTemplates: any = [];
    private unsubscribe: ReplaySubject<void> = new ReplaySubject<void>();

    private modalRef: NgbModalRef;

/* --------------------------------------------------- LIFE CYCLE --------------------------------------------------- */

    constructor(private sectionTemplateService: SectionTemplateService,
                private modalService: NgbModal,
                private toastService: ToastService,
                private router: Router){

    }

    ngOnInit(): void {
        this.getAllSectionTemplates();
    }


    ngOnDestroy(): void {
      if (this.modalRef) {
        this.modalRef.close();
      }
    }

/* ---------------------------------------------------- FUNCTIONS --------------------------------------------------- */
    /**
     * Retrieves all section templates from database
     */
    getAllSectionTemplates(){
        this.sectionTemplateService.getSectionTemplates().pipe(takeUntil(this.unsubscribe))
        .subscribe((apiResponse: APIGetMultiResponse<RenderResult>) => {
            this.sectionTemplates = apiResponse.results;
        });
    }


    /**
     * Displays a modal view for user to confirm deletion of section template
     * @param sectionTemplate instance of section template which should be deleted
     */
    showDeleteModal(sectionTemplate: CmdbSectionTemplate){
        this.modalRef = this.modalService.open(SectionTemplateDeleteModalComponent, { size: 'lg' });
        this.modalRef.componentInstance.sectionTemplate = sectionTemplate;

        this.modalRef.result.then((sectionTemplateID: number) => {
            //Delete the section template
            if(sectionTemplateID > 0){
                this.sectionTemplateService.deleteSectionTemplate(sectionTemplateID).subscribe((res: any) => {
                    this.toastService.success("Section Template with ID " + sectionTemplateID  + " deleted!");
                    this.getAllSectionTemplates();
                }, error => {
                  this.toastService.error(error);
                });
            }
        });
    }

    /**
     * Displays a modal view for user to confirm transformation of 
     * section template to a global section template
     * 
     * @param sectionTemplate instance of section template which should be transformed
     */
    showTransformModal(sectionTemplate: CmdbSectionTemplate){
        this.modalRef = this.modalService.open(SectionTemplateTransformModalComponent, { size: 'lg' });
        this.modalRef.componentInstance.sectionTemplate = sectionTemplate;

        this.modalRef.result.then((sectionTemplateID: number) => {
            //Delete the section template
            if(sectionTemplateID > 0){
                let params = {
                    'name': sectionTemplate.name,
                    'label': sectionTemplate.label,
                    'type': 'section',
                    'is_global': true,
                    'fields': JSON.stringify(sectionTemplate.fields),
                    'public_id': sectionTemplate.public_id
                }


                this.sectionTemplateService.updateSectionTemplate(params).subscribe((res: APIUpdateSingleResponse) => {
                    this.toastService.success(`Section Template with ID: ${sectionTemplate.public_id} transformed 
                                            to a Global Section Template!`);
                    this.getAllSectionTemplates();
                }, error => {
                  this.toastService.error(error);
                });
            }
        });
    }
}