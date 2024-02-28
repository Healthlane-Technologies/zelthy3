import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useState, useEffect } from 'react';

import { useField, Formik, FieldArray, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { get } from 'lodash';
import { transformToFormDataOrder } from '../../../../utils/helper';
import useApi from '../../../../hooks/useApi';

import { useSelector, useDispatch } from 'react-redux';
import {
	closeIsEditPolicyModalOpen,
	selectAppPoliciesManagementFormData,
	selectIsEditPolicyModalOpen,
	toggleRerenderPage,
} from '../../slice';

import { ReactComponent as ModalCloseIcon } from '../../../../assets/images/svg/modal-close-icon.svg';
import { useParams } from 'react-router-dom';

const EditPolicyForm = ({ closeModal }) => {
	let { appId } = useParams();
	const dispatch = useDispatch();

	const appPoliciesManagementFormData = useSelector(
		selectAppPoliciesManagementFormData
	);
	const triggerApi = useApi();
	let initialValues = {
		name: appPoliciesManagementFormData?.name ?? '',
		description: appPoliciesManagementFormData?.description ?? '',
	};

	let validationSchema = Yup.object({
		name: Yup.string().required('Required'),
		description: Yup.string().required('Required'),
	});

	let onSubmit = (values) => {
		let tempValues = values;
		if (tempValues['phone']) {
			tempValues['phone'] = '+91' + tempValues['phone'];
		}

		let dynamicFormData = transformToFormDataOrder(tempValues);

		const makeApiCall = async () => {
			const { response, success } = await triggerApi({
				url: `/api/v1/apps/${appId}/policies/${appPoliciesManagementFormData?.id}/`,
				type: 'PUT',
				loader: true,
				payload: dynamicFormData,
			});

			if (success && response) {
				closeModal();
				dispatch(toggleRerenderPage());
			}
		};

		makeApiCall();
	};

	return (
		<Formik
			initialValues={initialValues}
			validationSchema={validationSchema}
			onSubmit={onSubmit}
		>
			{(formik) => {
				return (
					<form
						className="complete-hidden-scroll-style flex grow flex-col gap-4 overflow-y-auto"
						onSubmit={formik.handleSubmit}
					>
						<div className="flex grow flex-col gap-[24px]">
							<div className="flex grow flex-col gap-[24px]">
								<div className="flex flex-col gap-[4px]">
									<label
										htmlFor="name"
										className="font-lato text-form-xs font-semibold text-[#A3ABB1]"
									>
										Policy Name
									</label>
									<input
										id="name"
										name="name"
										type="text"
										onChange={formik.handleChange}
										onBlur={formik.handleBlur}
										value={formik.values.name}
										className="rounded-[6px] border border-[#DDE2E5] px-[16px] py-[14px] font-lato placeholder:text-[#9A9A9A] hover:outline-0 focus:outline-0"
										placeholder="Enter policy name"
									/>
									{formik.touched.name && formik.errors.name ? (
										<div className="font-lato text-form-xs text-[#cc3300]">
											{formik.errors.name}
										</div>
									) : null}
								</div>
								<div className="flex flex-col gap-[4px]">
									<label
										htmlFor="description"
										className="font-lato text-form-xs font-semibold text-[#A3ABB1]"
									>
										Policy Description
									</label>
									<textarea
										id="description"
										name="description"
										type="text"
										onChange={formik.handleChange}
										onBlur={formik.handleBlur}
										value={formik.values.description}
										className="rounded-[6px] border border-[#DDE2E5] px-[16px] py-[14px] font-lato placeholder:text-[#9A9A9A] hover:outline-0 focus:outline-0"
										placeholder="Enter policy Description"
									/>
									{formik.touched.description && formik.errors.description ? (
										<div className="font-lato text-form-xs text-[#cc3300]">
											{formik.errors.description}
										</div>
									) : null}
								</div>
							</div>
						</div>
						<div className="sticky bottom-0 flex flex-col gap-[8px] bg-[#ffffff] pt-[24px] font-lato text-[#696969]">
							<button
								type="submit"
								className="flex w-full items-center justify-center rounded-[4px] bg-primary px-[16px] py-[10px] font-lato text-[14px] font-bold leading-[20px] text-white disabled:opacity-[0.38]"
								// disabled={!(formik.isValid && formik.dirty)}
							>
								<span>Save</span>
							</button>
						</div>
					</form>
				);
			}}
		</Formik>
	);
};

export default function EditPolicyModal() {
	const isEditPolicyModalOpen = useSelector(selectIsEditPolicyModalOpen);
	const dispatch = useDispatch();

	function closeModal() {
		dispatch(closeIsEditPolicyModalOpen());
	}

	return (
		<>
			<Transition appear show={isEditPolicyModalOpen} as={Fragment}>
				<Dialog as="div" className="relative z-10" onClose={() => {}}>
					<Transition.Child
						as={Fragment}
						enter="ease-in-out duration-700"
						enterFrom="opacity-0"
						enterTo="opacity-100"
						leave="ease-in-out duration-700"
						leaveFrom="opacity-100"
						leaveTo="opacity-0"
					>
						<div className="fixed inset-0 bg-black bg-opacity-[.67]" />
					</Transition.Child>

					<Transition.Child
						as={Fragment}
						enter="transform transition ease-in-out duration-500"
						enterFrom="translate-x-full"
						enterTo="translate-x-0"
						leave="transform transition ease-in-out duration-500"
						leaveFrom="translate-x-0"
						leaveTo="translate-x-full"
					>
						<div className="fixed inset-0 overflow-y-auto">
							<div className="flex h-screen max-h-screen min-h-full grow items-center justify-center text-center md:justify-end">
								<Dialog.Panel className="relative flex h-screen max-h-screen min-h-full w-full max-w-[498px] transform flex-col gap-[32px] overflow-hidden bg-white px-[24px] pt-[52px] pb-[40px] text-left align-middle shadow-xl transition-all md:pl-[32px] md:pr-[72px] md:pt-[32px]">
									<div className="flex justify-end md:absolute md:top-0 md:right-0">
										<button
											type="button"
											className="flex justify-end focus:outline-none md:absolute md:top-[16px] md:right-[16px]"
											onClick={closeModal}
										>
											<ModalCloseIcon />
										</button>
									</div>
									<Dialog.Title as="div" className="flex flex-col gap-2">
										<div className="flex flex-col gap-[2px]">
											<h4 className="font-source-sans-pro text-[22px] font-semibold leading-[28px]">
												Edit Policy
											</h4>
										</div>
									</Dialog.Title>
									<EditPolicyForm closeModal={closeModal} />
								</Dialog.Panel>
							</div>
						</div>
					</Transition.Child>
				</Dialog>
			</Transition>
		</>
	);
}
