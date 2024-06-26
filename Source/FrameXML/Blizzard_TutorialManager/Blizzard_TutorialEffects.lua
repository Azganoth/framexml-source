

-- ------------------------------------------------------------------------------------------------------------
TutorialQuestBangGlow = {};
function TutorialQuestBangGlow:Show(button)
	if not self.framePool then
		self.framePool = CreateFramePool("FRAME", nil, "TutorialQuestBangGlowTemplate");
	end

	local frame = self:GetExisting(button);
	if frame then
		return;
	end
	local icon = button.Icon;
	frame = self.framePool:Acquire();
	frame.button = button;
	frame:SetParent(button);
	frame:ClearAllPoints();
	frame:SetFrameStrata("DIALOG");
	frame:SetPoint("CENTER", icon, 0, 0);
	frame.GlowAnim:Play();
	frame:Show();
end

function TutorialQuestBangGlow:Hide(button)
	local frame = self:GetExisting(button);
	if frame then
		frame.GlowAnim:Stop();
		self.framePool:Release(frame);
	end
end

function TutorialQuestBangGlow:GetExisting(button)
	if not self.framePool then
		return;
	end
	for frame in self.framePool:EnumerateActive() do
		if frame.button == button then
			return frame;
		end
	end
end

-- ------------------------------------------------------------------------------------------------------------
TutorialDragButton = {};
function TutorialDragButton:Show(originButton, destButton)
	self:Hide();
	Dispatcher:RegisterEvent("OnUpdate", self);

	local texture;
	if originButton.icon then
		texture = originButton.icon:GetTexture();
	else
		local slot = SpellBook_GetSpellBookSlot(originButton);
		if slot then
			if originButton.spellID then -- the data is set if this is from a flyout spell button
				texture = GetSpellTexture(originButton.spellID);
			else
				texture = GetSpellBookItemTexture(slot, SpellBookFrame.bookType);
			end
		end
	end

	local originFrame = TutorialDragOriginFrame;
	originFrame:SetParent(originButton.DragButton or originButton);
	originFrame:SetPoint("CENTER");
	originFrame:Show();

	local targetFrame = TutorialDragTargetFrame;
	targetFrame:SetParent(destButton:GetParent());
	targetFrame:SetPoint("CENTER", destButton);
	targetFrame:Show();

	local animFrame = TutorialDragAnimationFrame;
	animFrame.Icon:SetTexture(texture);
	
	animFrame:SetParent(UIParent);
	animFrame:SetFrameStrata("DIALOG");
	animFrame:ClearAllPoints();
	animFrame:SetPoint("CENTER", originButton.DragButton or originButton);
	animFrame:Show();

	self.originFrame = originButton.DragButton or originButton;
	self.destFrame = destButton;
	self:Animate();
end

function TutorialDragButton:Animate()
	local animFrame = TutorialDragAnimationFrame;
	animFrame.Anim:Stop();

	self.ox, self.oy = self.originFrame:GetCenter();
	self.tx, self.ty = self.destFrame:GetCenter();

	animFrame.Anim.Move:SetOffset(self.tx - self.ox, self.ty - self.oy);
	animFrame.Anim:Play();
end

function TutorialDragButton:OnUpdate()
	local ox, oy = self.originFrame:GetCenter();
	local tx, ty = self.destFrame:GetCenter();

	if (ox ~= self.ox) or (oy ~= self.oy) or (tx ~= self.tx) or (ty ~= self.ty) then
		self:Animate();
	end
end

function TutorialDragButton:Hide()
	Dispatcher:UnregisterEvent("OnUpdate", self);
	TutorialDragOriginFrame:Hide();
	TutorialDragTargetFrame:Hide();
	TutorialDragAnimationFrame:Hide();
end
-- ------------------------------------------------------------------------------------------------------------
