
ExtraActionButtonPriority = 100;
ZoneAbilityFramePriority = 200;


ExtraAbilityContainerMixin = {};

function ExtraAbilityContainerMixin:OnLoad()
	self.frames = {};
	self:Layout();
end

function ExtraAbilityContainerMixin:OnShow()
	LayoutMixin.OnShow(self);
	UIParentManagedFrameMixin.OnShow(self);
end

function ExtraAbilityContainerMixin:OnHide()
	UIParentManagedFrameMixin.OnHide(self);
end

local function SortFramePairs(lhsFramePair, rhsFramePair)
	return lhsFramePair.priority < rhsFramePair.priority;
end

function ExtraAbilityContainerMixin:AddFrame(frameToAdd, priority)
	local bestSlot = nil;
	for i, framePair in ipairs(self.frames) do
		if framePair.frame == frameToAdd then
			if framePair.priority == priority then
				return;
			end

			framePair.priority = priority;
			table.sort(self.frames, SortFramePairs);
			self:UpdateLayoutIndicies();
			return;
		elseif not bestSlot and framePair.priority >= priority then
			bestSlot = i;
		end
	end

	if not bestSlot then
		bestSlot = #self.frames + 1;
	end

	frameToAdd:SetParent(self);
	table.insert(self.frames, bestSlot, {frame = frameToAdd, priority = priority});
	frameToAdd:Show();

	self:UpdateLayoutIndicies();
	self:UpdateShownState();
end

function ExtraAbilityContainerMixin:RemoveFrame(frameToRemove)
	for i, framePair in ipairs(self.frames) do
		if framePair.frame == frameToRemove then
			frameToRemove.layoutIndex = nil;
			frameToRemove:SetParent(nil);
			table.remove(self.frames, i);
			frameToRemove:Hide();
			break;
		end
	end

	self:UpdateLayoutIndicies();
	self:UpdateShownState();
end

function ExtraAbilityContainerMixin:UpdateLayoutIndicies()
	for i, framePair in ipairs(self.frames) do
		framePair.frame.layoutIndex = i;
	end

	self:MarkDirty();
end

function ExtraAbilityContainerMixin:UpdateShownState()
	self:SetShown(self.isInEditMode or #self.frames > 0);
end
