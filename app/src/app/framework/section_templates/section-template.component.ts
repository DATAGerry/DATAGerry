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
import { Component, OnDestroy, OnInit } from '@angular/core';

import { takeUntil } from 'rxjs/operators';
import { ReplaySubject } from 'rxjs';

import { v4 as uuidv4 } from 'uuid';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';

import { SectionTemplateService } from './services/section-template.service';
import { ToastService } from 'src/app/layout/toast/toast.service';

import { RenderResult } from '../models/cmdb-render';
import { APIGetMultiResponse, APIInsertSingleResponse, APIUpdateSingleResponse } from 'src/app/services/models/api-response';
import { SectionTemplateDeleteModalComponent } from './layout/modals/section-template-delete/section-template-delete-modal.component';
import { CmdbSectionTemplate, Field } from '../models/cmdb-section-template';
import { SectionTemplateTransformModalComponent } from './layout/modals/section-template-transform/section-template-transform-modal.component';
import { SectionTemplateCloneModalComponent } from './layout/modals/section-template-clone/section-template-clone-modal.component';
import { PreviewModalComponent } from '../type/builder/modals/preview-modal/preview-modal.component';
/* ------------------------------------------------------------------------------------------------------------------ */

export interface GlobalTemplateCounts {
    'types': number,
    'objects': number
}

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

    constructor(
        private sectionTemplateService: SectionTemplateService,
        private modalService: NgbModal,
        private toastService: ToastService){

    }


    ngOnInit(): void {
        this.getAllSectionTemplates();
    }


    ngOnDestroy(): void {
        if (this.modalRef) {
            this.modalRef.close();
        }
    }

/* -------------------------------------------------- API FUNCTIONS ------------------------------------------------- */

    /**
     * Retrieves all section templates from database
     */
    getAllSectionTemplates(){
        this.sectionTemplateService.getSectionTemplates().pipe(takeUntil(this.unsubscribe))
        .subscribe((apiResponse: APIGetMultiResponse<CmdbSectionTemplate>) => {
            this.sectionTemplates = apiResponse.results;
        },
        apiResponse => this.toastService.error(apiResponse.error)
        );
    }

/* ------------------------------------------------- MODAL HANDLING ------------------------------------------------- */

    /**
     * Displays a modal view for user to confirm deletion of section template
     * @param sectionTemplate instance of section template which should be deleted
     */
    showDeleteModal(sectionTemplate: CmdbSectionTemplate){

        this.sectionTemplateService.getGlobalSectionTemplateCount(sectionTemplate.public_id).subscribe((response: GlobalTemplateCounts) => {
            let counts: GlobalTemplateCounts = response

            this.modalRef = this.modalService.open(SectionTemplateDeleteModalComponent, { size: 'lg' });
            this.modalRef.componentInstance.sectionTemplate = sectionTemplate;
            this.modalRef.componentInstance.templateCounts = counts;
    
            this.modalRef.result.then((sectionTemplateID: number) => {
                //Delete the section template
                if(sectionTemplateID > 0){
                    this.sectionTemplateService.deleteSectionTemplate(sectionTemplateID).subscribe((res: any) => {
                        this.toastService.success("Section Template with ID " + sectionTemplateID  + " deleted!");
                        this.getAllSectionTemplates();
                    },
                    res => this.toastService.error(res.error)
                    );
                }
            });
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
                    'predefined': false,
                    'fields': JSON.stringify(sectionTemplate.fields),
                    'public_id': sectionTemplate.public_id
                }

                this.sectionTemplateService.updateSectionTemplate(params).subscribe((res: APIUpdateSingleResponse) => {
                    this.toastService.success(`Section Template with ID: ${sectionTemplate.public_id} transformed 
                                            to a Global Section Template!`);
                    this.getAllSectionTemplates();
                },
                res => this.toastService.error(res.error)
                );
            }
        });
    }


    /**
     * Displays a modal view for user to clone a section template
     * 
     * @param sectionTemplate instance of section template which should be cloned
     */
    public showCloneModal(sectionTemplate: CmdbSectionTemplate){
        this.modalRef = this.modalService.open(SectionTemplateCloneModalComponent, { size: 'lg' });
        this.modalRef.componentInstance.sectionTemplate = sectionTemplate;

        this.modalRef.result.then((values: any) => {
            if(values){

                const updatedFields: Field[] = this.setNewFieldIDs(sectionTemplate.fields);

                let params = {
                    'name': sectionTemplate.name,
                    'label': values.templateLabel,
                    'type': 'section',
                    'is_global': values.isGlobal,
                    'predefined': false,
                    'fields': JSON.stringify(updatedFields)
                }

                params.name = this.generateSectionTemplateName(values.isGlobal);

                this.sectionTemplateService.postSectionTemplate(params).subscribe((res: APIInsertSingleResponse) => {
                    this.toastService.success("Section Template cloned!");
                    this.getAllSectionTemplates();
                }, error => {
                    console.log("error in clone section template response");
                    this.toastService.error(error);
                });
            }
        });
    }


    /**
     * Displays a preview of a section template with all fields
     * 
     * @param sectionTemplate The section template which should be previewed
     */
    public showTemplatePreview(sectionTemplate: CmdbSectionTemplate){
        const previewModal = this.modalService.open(PreviewModalComponent, { scrollable: true });
        previewModal.componentInstance.sections = [sectionTemplate];
    }

/* ------------------------------------------------ HELPER FUNCTIONS ------------------------------------------------ */

    /**
     * Creates new IDs for fields
     * 
     * @param fields Fields which require new IDs
     * @returns The given fields with new IDs
     */
    private setNewFieldIDs(fields: Field[]){
        for(let field of fields){
            field.name = this.generateFieldName(field.type);
        }

        return fields;
    }


    /**
     * Retrives the label for the "Type" column of the table
     * @param sectionTemplate The template for which the label should be calculated
     * @returns (string): Type name for the given section template
     */
    public getTemplateTypeLabel(sectionTemplate: CmdbSectionTemplate): string{
        if(sectionTemplate.predefined){
            return "Predefined";
        }

        if(sectionTemplate.is_global){
            return "Global";
        }

        return "Standard";
    }


    /**
     * Generates a new name for a field
     * @param fieldType Type of the field
     */
    private generateFieldName(fieldType: string){
        return `${fieldType}-${uuidv4()}`
    }


    /**
     * Generates a unique name for section templates
     * 
     * @returns unique name for section templates
     */
    public generateSectionTemplateName(isGlobal:boolean = false){
        if(isGlobal){
            return `dg_gst-${uuidv4()}`;
        }

        return `section_template-${uuidv4()}`;
    }
}
