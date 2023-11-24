<?php

namespace Src\Auth;

interface IdentityInterface
{
    public function findIdentity(int $id):self;

    public function getId(): int;

    public function attemptIdentity(array $credentials);
}
