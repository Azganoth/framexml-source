if IsMacClient() then
	DefineGameSettingsMacOpenUniversalAccessDialog(StaticPopupDialogs);
	DefineGameSettingsMacOpenInputMonitoringDialog(StaticPopupDialogs);

	SettingsRegistrar:AddRegistrant(RegisterMacSettings);
end
